(() => {
  // Paste your Google OAuth 2.0 Web Client ID below (or set GOOGLE_CLIENT_ID in server.py / env):
  const GOOGLE_CLIENT_ID = "998989575243-qk50h87i19kiuu1cnl0rrv6sjt8ruka3.apps.googleusercontent.com";

  const state = {
    problems: [],
    currentProblem: null,
    currentProblemId: null,
    selectedSampleIndex: 0,
    drawerFilterTier: "All",
    drawerSearch: "",
    fontSize: parseInt(localStorage.getItem("col1000_font_size") || "14", 10),
    theme: localStorage.getItem("col1000_theme") || "dark",
    user: JSON.parse(localStorage.getItem("col1000_user") || "null"),
    googleClientId: "",
    cmEditor: null,
    usingFallbackEditor: false,
    hintsRevealed: {}, // { [problemId]: 0 | 1 | 2 }
    guestSolvedIds: new Set(JSON.parse(localStorage.getItem("col1000_guest_solved") || "[]")),
    pdfDoc: null,
    pdfScale: 1.25,
    pdfRenderToken: 0,
    isRunning: false,
  };

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  function escapeHtml(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function formatRichText(text) {
    if (!text) return "";
    const codeTokens = [];
    let html = escapeHtml(text).replace(/`([^`]+)`/g, (_, code) => {
      const idx = codeTokens.length;
      codeTokens.push(`<code class="inline-code">${code}</code>`);
      return `\u0000CODE${idx}\u0000`;
    });
    html = html
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/\*([^*\n]+)\*/g, "<em>$1</em>")
      .replace(/\n/g, "<br>");
    return html.replace(/\u0000CODE(\d+)\u0000/g, (_, idx) => codeTokens[Number(idx)]);
  }

  function authHeaders() {
    const h = { "Content-Type": "application/json" };
    if (state.user && state.user.id) {
      h["X-User-Id"] = state.user.id;
    }
    return h;
  }

  async function apiGet(url) {
    const res = await fetch(url, { headers: authHeaders() });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  async function apiPost(url, body) {
    const res = await fetch(url, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
    return data;
  }

  // Theme
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("col1000_theme", theme);
    $("#themeIconSun").classList.toggle("hidden", theme === "dark");
    $("#themeIconMoon").classList.toggle("hidden", theme === "light");
    if (state.cmEditor) {
      state.cmEditor.setOption("theme", theme === "dark" ? "material-darker" : "eclipse");
    }
  }

  // Editor abstraction
  function initEditor() {
    const container = $("#editorContainer");
    if (window.CodeMirror) {
      state.cmEditor = window.CodeMirror(container, {
        value: "",
        mode: "python",
        theme: state.theme === "dark" ? "material-darker" : "eclipse",
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        smartIndent: true,
        matchBrackets: true,
        extraKeys: {
          Tab: (cm) => {
            if (cm.somethingSelected()) {
              cm.indentSelection("add");
            } else {
              cm.replaceSelection("    ", "end");
            }
          },
          "Ctrl-Enter": () => handleRun(),
          "Cmd-Enter": () => handleRun(),
          "Ctrl-Shift-Enter": () => handleSubmit(),
          "Cmd-Shift-Enter": () => handleSubmit(),
        },
      });
      state.cmEditor.on("change", () => saveDraftCode());
      applyFontSize(state.fontSize);
    } else {
      state.usingFallbackEditor = true;
      const wrap = $("#fallbackEditorWrap");
      const ta = $("#fallbackTextarea");
      wrap.classList.remove("hidden");
      ta.addEventListener("input", () => {
        updateFallbackLineNumbers();
        saveDraftCode();
      });
      ta.addEventListener("scroll", () => {
        $("#fallbackLineNumbers").scrollTop = ta.scrollTop;
      });
      ta.addEventListener("keydown", (e) => {
        if (e.key === "Tab") {
          e.preventDefault();
          const start = ta.selectionStart;
          const end = ta.selectionEnd;
          ta.value = ta.value.slice(0, start) + "    " + ta.value.slice(end);
          ta.selectionStart = ta.selectionEnd = start + 4;
          updateFallbackLineNumbers();
          saveDraftCode();
        } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          if (e.shiftKey) handleSubmit();
          else handleRun();
        } else if (e.key === "Enter") {
          const start = ta.selectionStart;
          const lineStart = ta.value.lastIndexOf("\n", start - 1) + 1;
          const currentLine = ta.value.slice(lineStart, start);
          const indentMatch = currentLine.match(/^(\s*)/);
          let indent = indentMatch ? indentMatch[1] : "";
          if (currentLine.trimEnd().endsWith(":")) indent += "    ";
          if (indent) {
            e.preventDefault();
            const end = ta.selectionEnd;
            ta.value = ta.value.slice(0, start) + "\n" + indent + ta.value.slice(end);
            ta.selectionStart = ta.selectionEnd = start + 1 + indent.length;
            updateFallbackLineNumbers();
            saveDraftCode();
          }
        }
      });
      applyFontSize(state.fontSize);
    }
  }

  function updateFallbackLineNumbers() {
    const ta = $("#fallbackTextarea");
    const count = Math.max(1, ta.value.split("\n").length);
    $("#fallbackLineNumbers").textContent = Array.from({ length: count }, (_, i) => i + 1).join("\n");
  }

  function getEditorCode() {
    if (state.cmEditor) return state.cmEditor.getValue();
    return $("#fallbackTextarea").value;
  }

  function setEditorCode(code) {
    if (state.cmEditor) {
      state.cmEditor.setValue(code || "");
    } else {
      $("#fallbackTextarea").value = code || "";
      updateFallbackLineNumbers();
    }
  }

  function applyFontSize(px) {
    const clamped = Math.max(11, Math.min(22, px));
    state.fontSize = clamped;
    localStorage.setItem("col1000_font_size", String(clamped));
    $("#fontSizeLabel").textContent = `${clamped}px`;
    if (state.cmEditor) {
      state.cmEditor.getWrapperElement().style.fontSize = `${clamped}px`;
      state.cmEditor.refresh();
    } else {
      $("#fallbackTextarea").style.fontSize = `${clamped}px`;
      $("#fallbackLineNumbers").style.fontSize = `${clamped}px`;
    }
  }

  function draftKey(pid) {
    const uid = state.user ? state.user.id : "guest";
    return `col1000_draft_${uid}_${pid}`;
  }

  function saveDraftCode() {
    if (!state.currentProblemId) return;
    localStorage.setItem(draftKey(state.currentProblemId), getEditorCode());
  }

  // Tabs
  function switchLeftTab(tabName) {
    $$("[data-left-tab]").forEach((btn) =>
      btn.classList.toggle("active", btn.dataset.leftTab === tabName)
    );
    $$(".left-pane .tab-panel").forEach((panel) =>
      panel.classList.toggle("active", panel.id === `tab-${tabName}`)
    );
    if (tabName === "submissions") {
      loadSubmissions();
    }
  }

  function switchConsoleTab(tabName) {
    $$("[data-console-tab]").forEach((btn) =>
      btn.classList.toggle("active", btn.dataset.consoleTab === tabName)
    );
    $$(".console-tab-panel").forEach((panel) =>
      panel.classList.toggle("active", panel.id === `console-${tabName}`)
    );
  }

  // Drawer
  function toggleDrawer(open) {
    const drawer = $("#problemDrawer");
    const backdrop = $("#drawerBackdrop");
    const shouldOpen = typeof open === "boolean" ? open : !drawer.classList.contains("open");
    drawer.classList.toggle("open", shouldOpen);
    backdrop.classList.toggle("hidden", !shouldOpen);
    drawer.setAttribute("aria-hidden", String(!shouldOpen));
  }

  function renderDrawerList() {
    const list = $("#drawerList");
    const q = state.drawerSearch.trim().toLowerCase();
    const filtered = state.problems.filter((p) => {
      if (state.drawerFilterTier !== "All" && p.difficulty_tier !== state.drawerFilterTier) {
        return false;
      }
      if (q && !p.title.toLowerCase().includes(q) && !String(p.id).includes(q)) {
        return false;
      }
      return true;
    });

    const solvedCount = state.problems.filter((p) => p.solved).length;
    $("#solvedProgressPill").textContent = `${solvedCount}/${state.problems.length}`;

    if (!filtered.length) {
      list.innerHTML = `<div class="muted-text" style="padding: 16px;">No matching problems.</div>`;
      return;
    }

    list.innerHTML = filtered
      .map((p) => {
        const tierClass = `badge-${(p.difficulty_tier || "Medium").toLowerCase()}`;
        const activeClass = p.id === state.currentProblemId ? "active" : "";
        const check = p.solved
          ? `<span class="check-icon" title="Solved">&#10003;</span>`
          : `<span class="uncheck-icon">&#9675;</span>`;
        return `
          <button class="drawer-item ${activeClass}" data-prob-id="${p.id}">
            <div class="drawer-item-left">
              ${check}
              <span class="drawer-item-title">${p.id}. ${escapeHtml(p.title)}</span>
            </div>
            <span class="badge ${tierClass}">${escapeHtml(p.difficulty_tier)}</span>
          </button>
        `;
      })
      .join("");

    $$(".drawer-item").forEach((btn) => {
      btn.addEventListener("click", () => {
        const pid = parseInt(btn.dataset.probId, 10);
        toggleDrawer(false);
        selectProblem(pid);
      });
    });
  }

  // Load problems & render current problem
  async function loadProblemsList() {
    const data = await apiGet("/api/problems");
    state.problems = (data.problems || []).map((p) => ({
      ...p,
      solved: Boolean(p.solved || (!state.user && state.guestSolvedIds.has(p.id))),
    }));
    renderDrawerList();
  }

  async function selectProblem(pid, options = {}) {
    const previousCode = getEditorCode();
    const previousProb = state.currentProblem;
    const prob = await apiGet(`/api/problems/${pid}`);
    if (!state.user && state.guestSolvedIds.has(prob.id)) {
      prob.solved = true;
    }
    state.currentProblem = prob;
    state.currentProblemId = prob.id;
    state.selectedSampleIndex = 0;
    localStorage.setItem("col1000_last_problem", String(prob.id));

    // Title & Badges
    $("#probTitle").textContent = `${prob.id}. ${prob.title}`;
    const tier = prob.difficulty_tier || "Medium";
    const diffEl = $("#probDifficulty");
    diffEl.textContent = tier;
    diffEl.className = `badge badge-${tier.toLowerCase()}`;
    $("#probSolvedBadge").classList.toggle("hidden", !prob.solved);

    // Description sections
    $("#probStatement").innerHTML = formatRichText(prob.statement || "");
    const hasWorked = Boolean(prob.worked_example && prob.worked_example.trim());
    $("#workedExampleSection").classList.toggle("hidden", !hasWorked);
    $("#probWorkedExample").innerHTML = formatRichText(prob.worked_example || "");
    $("#probInputFormat").innerHTML = formatRichText(prob.input_format || "");
    $("#probOutputFormat").innerHTML = formatRichText(prob.output_format || "");
    $("#probConstraints").innerHTML = formatRichText(prob.constraints || "");

    // Sample tests in Description
    const samples = prob.sample_tests || [];
    $("#probSamplesList").innerHTML = samples
      .map(
        (s, idx) => `
        <div class="sample-item">
          <div class="sample-item-title">Sample ${idx + 1}</div>
          <div class="sample-io-grid">
            <div>
              <div class="io-label">Input</div>
              <pre class="mono-box">${escapeHtml(s.input)}</pre>
            </div>
            <div>
              <div class="io-label">Output</div>
              <pre class="mono-box">${escapeHtml(s.output)}</pre>
            </div>
          </div>
        </div>
      `
      )
      .join("");

    // Hints
    renderHints();

    // Solution
    const steps = prob.solution_steps || [];
    $("#solutionStepsList").innerHTML = steps
      .map((st) => `<li>${formatRichText(st)}</li>`)
      .join("");
    $("#solutionCodeBlock").textContent = prob.solution_code || "";

    // Editor code (preserve unsaved code on auth switch, else saved draft or starter)
    const starter = prob.starter_code || "";
    const shouldPreserve =
      options.preserveUnsaved &&
      previousProb &&
      previousProb.id === prob.id &&
      previousCode.trim() !== "" &&
      previousCode !== (previousProb.starter_code || "");
    if (shouldPreserve) {
      setEditorCode(previousCode);
      saveDraftCode();
    } else {
      const savedDraft = localStorage.getItem(draftKey(prob.id));
      setEditorCode(savedDraft !== null ? savedDraft : starter);
    }

    // Console sample pills
    renderConsoleSampleCases();
    $("#resultsEmpty").classList.remove("hidden");
    $("#resultsContent").classList.add("hidden");
    $("#customOutputWrap").classList.add("hidden");

    // Stepper buttons
    const idx = state.problems.findIndex((p) => p.id === prob.id);
    $("#prevProbBtn").disabled = idx <= 0;
    $("#nextProbBtn").disabled = idx < 0 || idx >= state.problems.length - 1;

    renderDrawerList();
    if ($("#tab-submissions").classList.contains("active")) {
      loadSubmissions();
    }
  }

  function renderHints() {
    const prob = state.currentProblem;
    if (!prob) return;
    const hints = prob.hints || [];
    const revealedCount = state.hintsRevealed[prob.id] || 0;

    const btn1 = $("#revealHint1Btn");
    const btn2 = $("#revealHint2Btn");
    const body1 = $("#hint1Body");
    const body2 = $("#hint2Body");

    if (revealedCount >= 1 && hints[0]) {
      body1.innerHTML = formatRichText(hints[0]);
      body1.classList.remove("hidden");
      btn1.textContent = "Revealed";
      btn1.disabled = true;
      btn2.disabled = false;
    } else {
      body1.classList.add("hidden");
      btn1.textContent = "Reveal Hint 1";
      btn1.disabled = !hints[0];
      btn2.disabled = true;
    }

    if (revealedCount >= 2 && hints[1]) {
      body2.innerHTML = formatRichText(hints[1]);
      body2.classList.remove("hidden");
      btn2.textContent = "Revealed";
      btn2.disabled = true;
    } else {
      body2.classList.add("hidden");
      btn2.textContent = "Reveal Hint 2";
    }
  }

  function renderConsoleSampleCases() {
    const samples = (state.currentProblem && state.currentProblem.sample_tests) || [];
    const pillsEl = $("#sampleCasePills");
    const viewEl = $("#selectedSampleView");

    if (!samples.length) {
      pillsEl.innerHTML = "";
      viewEl.innerHTML = `<div class="muted-text">No sample test cases available.</div>`;
      return;
    }

    pillsEl.innerHTML = samples
      .map(
        (_, i) =>
          `<button class="case-pill ${i === state.selectedSampleIndex ? "active" : ""}" data-sample-idx="${i}">Sample ${i + 1}</button>`
      )
      .join("");

    $$(".case-pill").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.selectedSampleIndex = parseInt(btn.dataset.sampleIdx, 10);
        renderConsoleSampleCases();
      });
    });

    const cur = samples[state.selectedSampleIndex] || samples[0];
    viewEl.innerHTML = `
      <div class="sample-io-grid">
        <div>
          <div class="io-label">Input</div>
          <pre class="mono-box">${escapeHtml(cur.input)}</pre>
        </div>
        <div>
          <div class="io-label">Expected Output</div>
          <pre class="mono-box">${escapeHtml(cur.output)}</pre>
        </div>
      </div>
    `;
  }

  function setLoading(isRun, loading) {
    state.isRunning = loading;
    $("#runBtn").disabled = loading;
    $("#submitBtn").disabled = loading;
    $("#runSpinner").classList.toggle("hidden", !(loading && isRun));
    $("#submitSpinner").classList.toggle("hidden", !(loading && !isRun));
  }

  async function handleRun() {
    if (state.isRunning || !state.currentProblem) return;
    const isCustomTab = $("#console-custom").classList.contains("active");
    const code = getEditorCode();
    setLoading(true, true);

    try {
      if (isCustomTab) {
        const customInput = $("#customInputArea").value;
        const res = await apiPost("/api/run", {
          problem_id: state.currentProblem.id,
          code,
          custom_input: customInput,
        });
        const wrap = $("#customOutputWrap");
        wrap.classList.remove("hidden");
        wrap.innerHTML = `
          <div class="verdict-banner ${res.status === "OK" ? "accepted" : "failed"}">
            <span>${escapeHtml(res.status)}</span>
            <span>${res.runtime_ms} ms</span>
          </div>
          <div class="io-label">Standard Output</div>
          <pre class="mono-box">${escapeHtml(res.stdout || "(empty)")}</pre>
          ${res.stderr ? `<div class="io-label" style="margin-top:8px;">Stderr</div><pre class="mono-box" style="color:var(--rose);">${escapeHtml(res.stderr)}</pre>` : ""}
        `;
      } else {
        const res = await apiPost("/api/run", {
          problem_id: state.currentProblem.id,
          code,
        });
        renderTestResults(res, false);
        switchConsoleTab("results");
      }
    } catch (err) {
      renderErrorResult(err.message);
      switchConsoleTab("results");
    } finally {
      setLoading(true, false);
    }
  }

  async function handleSubmit() {
    if (state.isRunning || !state.currentProblem) return;
    const code = getEditorCode();
    setLoading(false, true);

    try {
      const res = await apiPost("/api/submit", {
        problem_id: state.currentProblem.id,
        code,
        user_id: state.user ? state.user.id : "guest",
      });
      renderTestResults(res, true);
      switchConsoleTab("results");
      if (res.status === "Accepted") {
        $("#probSolvedBadge").classList.remove("hidden");
        state.currentProblem.solved = true;
        if (!state.user) {
          state.guestSolvedIds.add(state.currentProblem.id);
          localStorage.setItem(
            "col1000_guest_solved",
            JSON.stringify(Array.from(state.guestSolvedIds))
          );
        }
        const localProb = state.problems.find((p) => p.id === state.currentProblem.id);
        if (localProb) localProb.solved = true;
        renderDrawerList();
        await loadProblemsList();
      }
      if ($("#tab-submissions").classList.contains("active")) {
        loadSubmissions();
      }
    } catch (err) {
      renderErrorResult(err.message);
      switchConsoleTab("results");
    } finally {
      setLoading(false, false);
    }
  }

  function renderErrorResult(msg) {
    $("#resultsEmpty").classList.add("hidden");
    const container = $("#resultsContent");
    container.classList.remove("hidden");
    container.innerHTML = `<div class="verdict-banner failed"><span>Error</span><span>${escapeHtml(msg)}</span></div>`;
  }

  function renderTestResults(res, isSubmit) {
    $("#resultsEmpty").classList.add("hidden");
    const container = $("#resultsContent");
    container.classList.remove("hidden");
    const isAccepted = res.status === "Accepted";
    const label = isSubmit ? "Submission" : "Sample Run";

    const cards = (res.results || [])
      .map((tc) => {
        const passCls = tc.passed ? "pass-tag" : "fail-tag";
        if (tc.is_hidden) {
          return `
            <div class="result-case-card">
              <div class="result-case-head">
                <span>Hidden Test Case #${tc.index}</span>
                <span class="${passCls}">${escapeHtml(tc.status)} (${tc.runtime_ms} ms)</span>
              </div>
              ${tc.stderr ? `<pre class="mono-box" style="color:var(--rose);">${escapeHtml(tc.stderr)}</pre>` : ""}
            </div>
          `;
        }
        return `
          <div class="result-case-card">
            <div class="result-case-head">
              <span>Test Case #${tc.index}</span>
              <span class="${passCls}">${escapeHtml(tc.status)} (${tc.runtime_ms} ms)</span>
            </div>
            <div class="sample-io-grid">
              <div>
                <div class="io-label">Input</div>
                <pre class="mono-box">${escapeHtml(tc.input)}</pre>
              </div>
              <div>
                <div class="io-label">Expected</div>
                <pre class="mono-box">${escapeHtml(tc.expected)}</pre>
              </div>
            </div>
            <div style="margin-top:6px;">
              <div class="io-label">Your Output</div>
              <pre class="mono-box">${escapeHtml(tc.actual || "(empty)")}</pre>
            </div>
            ${tc.stderr ? `<div style="margin-top:6px;"><div class="io-label">Stderr</div><pre class="mono-box" style="color:var(--rose);">${escapeHtml(tc.stderr)}</pre></div>` : ""}
          </div>
        `;
      })
      .join("");

    container.innerHTML = `
      <div class="verdict-banner ${isAccepted ? "accepted" : "failed"}">
        <span>${label}: ${escapeHtml(res.status)}</span>
        <span>${res.passed_count} / ${res.total_count} Passed &middot; ${res.runtime_ms} ms</span>
      </div>
      ${cards}
    `;
  }

  // Submissions history
  async function loadSubmissions() {
    if (!state.currentProblem) return;
    const uid = state.user ? state.user.id : "guest";
    const listEl = $("#submissionsList");
    listEl.innerHTML = `<div class="muted-text">Loading submissions...</div>`;
    try {
      const data = await apiGet(
        `/api/submissions?problem_id=${state.currentProblem.id}&user_id=${encodeURIComponent(uid)}`
      );
      const subs = data.submissions || [];
      if (!subs.length) {
        listEl.innerHTML = `<div class="muted-text">No submissions yet for this problem.</div>`;
        return;
      }
      listEl.innerHTML = subs
        .map((s) => {
          const cls = s.status === "Accepted" ? "accepted" : "failed";
          const dt = new Date(s.created_at).toLocaleString();
          return `
            <div class="sub-row">
              <div class="sub-meta">
                <span class="sub-status ${cls}">${escapeHtml(s.status)}</span>
                <span class="sub-details">${s.passed_count}/${s.total_count} passed &middot; ${s.runtime_ms} ms &middot; ${escapeHtml(dt)}</span>
              </div>
              <button class="btn btn-sm btn-secondary load-sub-btn" data-sub-id="${s.id}">Load Code</button>
            </div>
          `;
        })
        .join("");

      $$(".load-sub-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          const found = subs.find((x) => String(x.id) === btn.dataset.subId);
          if (found) {
            setEditorCode(found.code);
            saveDraftCode();
          }
        });
      });
    } catch (err) {
      listEl.innerHTML = `<div class="error-text">Failed to load submissions: ${escapeHtml(err.message)}</div>`;
    }
  }

  // Modals
  function openModal(id) {
    $(`#${id}`).classList.remove("hidden");
  }

  function clearPdfViewer() {
    state.pdfRenderToken += 1;
    const container = $("#pdfPagesContainer");
    if (container) {
      container.querySelectorAll("canvas").forEach((c) => {
        c.width = 0;
        c.height = 0;
      });
      container.innerHTML = "";
    }
    const status = $("#pdfStatusMsg");
    if (status) {
      status.textContent = "";
      status.classList.add("hidden");
    }
    $("#pdfPageIndicator")?.classList.add("hidden");
    $("#pdfZoomControls")?.classList.add("hidden");
    if (state.pdfDoc) {
      try {
        state.pdfDoc.destroy();
      } catch {
        // Ignore cleanup errors
      }
      state.pdfDoc = null;
    }
  }

  function closeModal(id) {
    $(`#${id}`).classList.add("hidden");
    if (id === "pdfModal") {
      clearPdfViewer();
    }
  }

  function ensurePdfJs() {
    if (window.pdfjsLib) {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc =
        "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
      return Promise.resolve(window.pdfjsLib);
    }
    return new Promise((resolve, reject) => {
      const existing = document.querySelector('script[data-pdfjs="true"]');
      if (existing) {
        existing.addEventListener("load", () => {
          if (window.pdfjsLib) {
            window.pdfjsLib.GlobalWorkerOptions.workerSrc =
              "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
            resolve(window.pdfjsLib);
          } else {
            reject(new Error("pdfjsLib unavailable"));
          }
        });
        existing.addEventListener("error", () => reject(new Error("Failed to load PDF.js")));
        return;
      }
      const script = document.createElement("script");
      script.src = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js";
      script.async = true;
      script.dataset.pdfjs = "true";
      const timer = setTimeout(() => reject(new Error("PDF.js load timeout")), 10000);
      script.onload = () => {
        clearTimeout(timer);
        if (window.pdfjsLib) {
          window.pdfjsLib.GlobalWorkerOptions.workerSrc =
            "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
          resolve(window.pdfjsLib);
        } else {
          reject(new Error("pdfjsLib unavailable"));
        }
      };
      script.onerror = () => {
        clearTimeout(timer);
        reject(new Error("Failed to load PDF.js"));
      };
      document.head.appendChild(script);
    });
  }

  async function renderPdfPages() {
    if (!state.pdfDoc) return;
    const token = ++state.pdfRenderToken;
    const container = $("#pdfPagesContainer");
    const status = $("#pdfStatusMsg");
    const total = state.pdfDoc.numPages;

    container.querySelectorAll("canvas").forEach((c) => {
      c.width = 0;
      c.height = 0;
    });
    container.innerHTML = "";

    $("#pdfPageIndicator").textContent = `${total} ${total === 1 ? "page" : "pages"}`;
    $("#pdfPageIndicator").classList.remove("hidden");
    $("#pdfZoomLabel").textContent = `${Math.round(state.pdfScale * 100)}%`;
    $("#pdfZoomControls").classList.remove("hidden");
    status.textContent = `Rendering ${total} pages...`;
    status.classList.remove("hidden");

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    for (let pageNum = 1; pageNum <= total; pageNum++) {
      if (token !== state.pdfRenderToken) return;
      const page = await state.pdfDoc.getPage(pageNum);
      if (token !== state.pdfRenderToken) return;

      const viewport = page.getViewport({ scale: state.pdfScale });
      const canvas = document.createElement("canvas");
      canvas.className = "pdf-page-canvas";
      canvas.width = Math.floor(viewport.width * dpr);
      canvas.height = Math.floor(viewport.height * dpr);
      canvas.style.width = `${Math.floor(viewport.width)}px`;
      canvas.style.height = `${Math.floor(viewport.height)}px`;
      container.appendChild(canvas);

      const ctx = canvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      await page.render({ canvasContext: ctx, viewport }).promise;
    }

    if (token === state.pdfRenderToken) {
      status.classList.add("hidden");
    }
  }

  async function renderHtmlBookletFallback() {
    const container = $("#pdfPagesContainer");
    const status = $("#pdfStatusMsg");
    $("#pdfPageIndicator").textContent = `${state.problems.length} problems`;
    $("#pdfPageIndicator").classList.remove("hidden");
    $("#pdfZoomControls").classList.add("hidden");
    status.textContent = "Loading formatted problem booklet...";
    status.classList.remove("hidden");

    try {
      const fullProblems = await Promise.all(
        state.problems.map((p) => apiGet(`/api/problems/${p.id}`))
      );
      status.classList.add("hidden");
      container.innerHTML = `
        <div class="pdf-fallback-booklet">
          <div class="pdf-booklet-banner">
            Inline PDF preview is unavailable; showing the formatted HTML problem booklet. You can still use <strong>Download PDF</strong> or <strong>Open in New Tab</strong> above.
          </div>
          ${fullProblems
            .map((p) => {
              const tier = p.difficulty_tier || "Medium";
              const samples = (p.sample_tests || [])
                .map(
                  (s, i) => `
                  <div class="sample-item" style="margin-top:8px;">
                    <div class="sample-item-title">Sample ${i + 1}</div>
                    <div class="sample-io-grid">
                      <div><div class="io-label">Input</div><pre class="mono-box">${escapeHtml(s.input)}</pre></div>
                      <div><div class="io-label">Output</div><pre class="mono-box">${escapeHtml(s.output)}</pre></div>
                    </div>
                  </div>`
                )
                .join("");
              return `
                <article class="pdf-booklet-item">
                  <div class="pdf-booklet-head">
                    <h4>${p.id}. ${escapeHtml(p.title)}</h4>
                    <span class="badge badge-${tier.toLowerCase()}">${escapeHtml(tier)}</span>
                  </div>
                  <div class="prose-block">${formatRichText(p.statement || "")}</div>
                  ${p.worked_example ? `<div class="prose-block"><strong>Worked Example:</strong><br>${formatRichText(p.worked_example)}</div>` : ""}
                  <div class="section-grid">
                    <div class="section-card"><h3>Input Format</h3><div class="prose-block" style="margin:0;">${formatRichText(p.input_format || "")}</div></div>
                    <div class="section-card"><h3>Output Format</h3><div class="prose-block" style="margin:0;">${formatRichText(p.output_format || "")}</div></div>
                  </div>
                  <div class="section-card"><h3>Constraints</h3><pre class="mono-box">${formatRichText(p.constraints || "")}</pre></div>
                  ${samples}
                </article>
              `;
            })
            .join("")}
        </div>
      `;
    } catch (err) {
      status.textContent = `Could not load booklet: ${err.message}`;
    }
  }

  async function openPdfModal() {
    clearPdfViewer();
    openModal("pdfModal");
    const status = $("#pdfStatusMsg");
    status.textContent = "Loading PDF viewer...";
    status.classList.remove("hidden");

    try {
      const pdfjsLib = await ensurePdfJs();
      const loadingTask = pdfjsLib.getDocument("/COL1000_Practice_Problems_v2.pdf");
      state.pdfDoc = await loadingTask.promise;
      await renderPdfPages();
    } catch {
      await renderHtmlBookletFallback();
    }
  }

  async function openLeaderboard() {
    openModal("leaderboardModal");
    const wrap = $("#leaderboardTableWrap");
    wrap.innerHTML = `<div class="muted-text">Loading leaderboard...</div>`;
    try {
      const data = await apiGet("/api/leaderboard");
      const rows = data.leaderboard || [];
      if (!rows.length) {
        wrap.innerHTML = `<div class="muted-text" style="padding:24px 8px;text-align:center;">No students on the leaderboard yet. Sign in with your Google account and solve problems to appear here!</div>`;
        return;
      }
      wrap.innerHTML = `
        <table class="lb-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Student</th>
              <th>Solved</th>
              <th>E / M / H</th>
              <th>Score</th>
              <th>Submissions</th>
            </tr>
          </thead>
          <tbody>
            ${rows
              .map((r) => {
                const avHtml =
                  r.avatar && r.avatar.startsWith("http")
                    ? `<img src="${escapeHtml(r.avatar)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" />`
                    : escapeHtml((r.avatar || r.name.slice(0, 2)).slice(0, 2).toUpperCase());
                return `
              <tr>
                <td><strong>${r.rank}</strong></td>
                <td>
                  <div class="lb-user-cell">
                    <div class="lb-avatar">${avHtml}</div>
                    <div>
                      <div><strong>${escapeHtml(r.name)}</strong></div>
                      <div style="font-size:11px;color:var(--text-muted);">${escapeHtml(r.email)}</div>
                    </div>
                  </div>
                </td>
                <td><strong>${r.solved_count}</strong></td>
                <td>${r.easy_count} / ${r.medium_count} / ${r.hard_count}</td>
                <td><strong>${r.score}</strong></td>
                <td>${r.submissions_count}</td>
              </tr>
            `;
              })
              .join("")}
          </tbody>
        </table>
      `;
    } catch (err) {
      wrap.innerHTML = `<div class="error-text">Failed to load leaderboard: ${escapeHtml(err.message)}</div>`;
    }
  }

  // Auth
  function updateAuthUI() {
    if (state.user) {
      $("#authBtnLabel").textContent = state.user.name.split(" ")[0];
      $("#authModalTitle").textContent = "Account";
      $("#authSignedOutView").classList.add("hidden");
      $("#authSignedInView").classList.remove("hidden");
      $("#profileName").textContent = state.user.name;
      $("#profileEmail").textContent = state.user.email;
      const av = $("#profileAvatar");
      if (state.user.avatar && state.user.avatar.startsWith("http")) {
        av.innerHTML = `<img src="${escapeHtml(state.user.avatar)}" alt="" style="width:100%;height:100%;object-fit:cover;" />`;
      } else {
        av.textContent = (state.user.avatar || state.user.name.slice(0, 2)).toUpperCase();
      }
      document.cookie = `col1000_uid=${encodeURIComponent(state.user.id)}; path=/; max-age=2592000`;
    } else {
      $("#authBtnLabel").textContent = "Sign In";
      $("#authModalTitle").textContent = "Sign In to COL1000";
      $("#authSignedOutView").classList.remove("hidden");
      $("#authSignedInView").classList.add("hidden");
      document.cookie = "col1000_uid=; path=/; max-age=0";
    }
  }

  function decodeJwtPayload(token) {
    try {
      const base64Url = token.split(".")[1];
      const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split("")
          .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
          .join("")
      );
      return JSON.parse(jsonPayload);
    } catch {
      return null;
    }
  }

  async function handleGoogleCredentialResponse(response) {
    const errEl = $("#authErrorMsg");
    errEl.classList.add("hidden");
    const decoded = decodeJwtPayload(response.credential);
    if (!decoded || !decoded.sub) {
      errEl.textContent = "Failed to decode Google credential.";
      errEl.classList.remove("hidden");
      return;
    }

    try {
      const res = await apiPost("/api/auth/google", { credential: response.credential });
      state.user = res.user;
    } catch {
      // Fallback to decoded JWT profile if backend verification is not yet configured
      state.user = {
        id: `google_${decoded.sub}`,
        name: decoded.name || decoded.email || "Google User",
        email: decoded.email || "",
        avatar: decoded.picture || "",
      };
    }

    localStorage.setItem("col1000_user", JSON.stringify(state.user));
    updateAuthUI();
    closeModal("authModal");
    await loadProblemsList();
    if (state.currentProblemId) {
      await selectProblem(state.currentProblemId, { preserveUnsaved: true });
    }
  }

  function mountGoogleSignInButton() {
    const clientId = state.googleClientId || GOOGLE_CLIENT_ID;
    const renderBtn = () => {
      if (window.google && window.google.accounts && window.google.accounts.id) {
        $("#googleGsiButton").innerHTML = "";
        window.google.accounts.id.initialize({
          client_id: clientId,
          ux_mode: "popup",
          callback: handleGoogleCredentialResponse,
        });
        window.google.accounts.id.renderButton($("#googleGsiButton"), {
          theme: state.theme === "dark" ? "filled_black" : "outline",
          size: "large",
          text: "signin_with",
          shape: "rectangular",
          width: 320,
        });
        return true;
      }
      return false;
    };

    if (renderBtn()) return;
    const existing = document.querySelector('script[src="https://accounts.google.com/gsi/client"]');
    if (existing) {
      existing.addEventListener("load", renderBtn);
      return;
    }
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = renderBtn;
    document.head.appendChild(script);
  }

  async function initAuthConfig() {
    try {
      const cfg = await apiGet("/api/config");
      const serverCid = (cfg.google_client_id || "").trim();
      state.googleClientId =
        serverCid && serverCid !== "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
          ? serverCid
          : GOOGLE_CLIENT_ID;
    } catch {
      state.googleClientId = GOOGLE_CLIENT_ID;
    }
    mountGoogleSignInButton();
  }

  // Draggable resizer
  function initResizer() {
    const resizer = $("#paneResizer");
    const leftPane = $(".left-pane");
    let dragging = false;

    resizer.addEventListener("mousedown", () => {
      dragging = true;
      document.body.style.cursor = "col-resize";
    });

    window.addEventListener("mousemove", (e) => {
      if (!dragging) return;
      const pct = (e.clientX / window.innerWidth) * 100;
      if (pct >= 24 && pct <= 70) {
        leftPane.style.width = `${pct}%`;
        if (state.cmEditor) state.cmEditor.refresh();
      }
    });

    window.addEventListener("mouseup", () => {
      if (dragging) {
        dragging = false;
        document.body.style.cursor = "";
      }
    });
  }

  // Event bindings
  function bindEvents() {
    $("#themeToggleBtn").addEventListener("click", () => {
      applyTheme(state.theme === "dark" ? "light" : "dark");
    });

    $("#drawerToggleBtn").addEventListener("click", () => toggleDrawer(true));
    $("#closeDrawerBtn").addEventListener("click", () => toggleDrawer(false));
    $("#drawerBackdrop").addEventListener("click", () => toggleDrawer(false));

    $("#drawerSearch").addEventListener("input", (e) => {
      state.drawerSearch = e.target.value;
      renderDrawerList();
    });

    $$(".filter-pill").forEach((btn) => {
      btn.addEventListener("click", () => {
        $$(".filter-pill").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.drawerFilterTier = btn.dataset.tier;
        renderDrawerList();
      });
    });

    $("#prevProbBtn").addEventListener("click", () => {
      const idx = state.problems.findIndex((p) => p.id === state.currentProblemId);
      if (idx > 0) selectProblem(state.problems[idx - 1].id);
    });

    $("#nextProbBtn").addEventListener("click", () => {
      const idx = state.problems.findIndex((p) => p.id === state.currentProblemId);
      if (idx >= 0 && idx < state.problems.length - 1) selectProblem(state.problems[idx + 1].id);
    });

    $$("[data-left-tab]").forEach((btn) =>
      btn.addEventListener("click", () => switchLeftTab(btn.dataset.leftTab))
    );
    $$("[data-console-tab]").forEach((btn) =>
      btn.addEventListener("click", () => switchConsoleTab(btn.dataset.consoleTab))
    );

    $("#revealHint1Btn").addEventListener("click", () => {
      if (!state.currentProblem) return;
      state.hintsRevealed[state.currentProblem.id] = Math.max(
        1,
        state.hintsRevealed[state.currentProblem.id] || 0
      );
      renderHints();
    });

    $("#revealHint2Btn").addEventListener("click", () => {
      if (!state.currentProblem) return;
      state.hintsRevealed[state.currentProblem.id] = 2;
      renderHints();
    });

    $("#copySolutionBtn").addEventListener("click", () => {
      if (!state.currentProblem) return;
      setEditorCode(state.currentProblem.solution_code || "");
      saveDraftCode();
    });

    $("#refreshSubmissionsBtn").addEventListener("click", () => loadSubmissions());

    $("#fontDecBtn").addEventListener("click", () => applyFontSize(state.fontSize - 1));
    $("#fontIncBtn").addEventListener("click", () => applyFontSize(state.fontSize + 1));

    $("#resetCodeBtn").addEventListener("click", () => {
      if (!state.currentProblem) return;
      setEditorCode(state.currentProblem.starter_code || "");
      localStorage.removeItem(draftKey(state.currentProblem.id));
    });

    $("#runBtn").addEventListener("click", handleRun);
    $("#submitBtn").addEventListener("click", handleSubmit);

    $("#viewPdfBtn").addEventListener("click", openPdfModal);
    $("#pdfZoomInBtn").addEventListener("click", () => {
      state.pdfScale = Math.min(2.5, Math.round((state.pdfScale + 0.2) * 100) / 100);
      renderPdfPages();
    });
    $("#pdfZoomOutBtn").addEventListener("click", () => {
      state.pdfScale = Math.max(0.6, Math.round((state.pdfScale - 0.2) * 100) / 100);
      renderPdfPages();
    });

    $("#leaderboardBtn").addEventListener("click", openLeaderboard);
    $("#authBtn").addEventListener("click", () => {
      updateAuthUI();
      if (!state.user) {
        mountGoogleSignInButton();
      }
      openModal("authModal");
    });

    $$(".modal-close").forEach((btn) => {
      btn.addEventListener("click", () => closeModal(btn.dataset.closeModal));
    });

    $$(".modal").forEach((modal) => {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal(modal.id);
      });
    });

    $("#signOutBtn").addEventListener("click", async () => {
      state.user = null;
      localStorage.removeItem("col1000_user");
      updateAuthUI();
      closeModal("authModal");
      await loadProblemsList();
      if (state.currentProblemId) selectProblem(state.currentProblemId);
    });
  }

  async function boot() {
    applyTheme(state.theme);
    updateAuthUI();
    initEditor();
    initResizer();
    bindEvents();
    await initAuthConfig();
    await loadProblemsList();

    const savedId = parseInt(localStorage.getItem("col1000_last_problem") || "1", 10);
    const initial =
      state.problems.find((p) => p.id === savedId) || state.problems[0];
    if (initial) {
      await selectProblem(initial.id);
    }
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
