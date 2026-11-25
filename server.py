#!/usr/bin/env python3
"""Backend HTTP server and Python code judge for IIT Delhi COL1000 Practice Platform."""

import hashlib
import json
import mimetypes
import os
import re
import sqlite3
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional, Tuple

from problems_data import PROBLEMS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "col1000.db")
PDF_PATH = os.path.join(BASE_DIR, "COL1000_Practice_Problems_v2.pdf")

PROBLEMS_BY_ID: Dict[int, Dict[str, Any]] = {int(p["id"]): p for p in PROBLEMS}
PROBLEMS_BY_SLUG: Dict[str, Dict[str, Any]] = {str(p["slug"]): p for p in PROBLEMS}

TIER_POINTS = {"Easy": 10, "Medium": 20, "Hard": 30}
EXEC_TIMEOUT_SEC = 3.0

# Paste your Google OAuth 2.0 Web Client ID below (or set the GOOGLE_CLIENT_ID env var):
GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "998989575243-qk50h87i19kiuu1cnl0rrv6sjt8ruka3.apps.googleusercontent.com",
).strip()


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                avatar TEXT DEFAULT '',
                is_demo INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                problem_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                passed_count INTEGER NOT NULL,
                total_count INTEGER NOT NULL,
                runtime_ms REAL NOT NULL,
                code TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_sub_user_prob ON submissions(user_id, problem_id)"
        )
        conn.commit()
    finally:
        conn.close()


CONFIG_PATH = os.path.join(BASE_DIR, "col1000_config.json")


def get_google_client_id() -> str:
    env_id = os.environ.get("GOOGLE_CLIENT_ID", "").strip()
    if env_id:
        return env_id
    return GOOGLE_CLIENT_ID


def save_google_client_id(client_id: str) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"google_client_id": client_id.strip()}, f, indent=2)


def normalize_exact(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def normalize_exact_preserve_leading(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines)


def normalize_unordered_lines(text: str) -> List[str]:
    lines = [
        line.strip()
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        if line.strip()
    ]
    return sorted(lines)


def normalize_strip_prompts(text: str) -> str:
    cleaned = text.replace("Enter n: ", "").replace("Enter k: ", "")
    return normalize_exact(cleaned)


def compare_output(actual: str, expected: str, judge_mode: str) -> bool:
    mode = judge_mode or "exact"
    if mode == "exact_preserve_leading":
        return normalize_exact_preserve_leading(actual) == normalize_exact_preserve_leading(expected)
    if mode == "unordered_lines":
        return normalize_unordered_lines(actual) == normalize_unordered_lines(expected)
    if mode == "strip_prompts":
        return normalize_strip_prompts(actual) == normalize_exact(expected)
    # "exact" and "driver" both compare using exact normalization
    return normalize_exact(actual) == normalize_exact(expected)


def run_python_code(code: str, stdin_data: str, timeout: float = EXEC_TIMEOUT_SEC) -> Tuple[str, str, float, str]:
    """Execute Python code in an isolated subprocess. Returns (stdout, stderr, runtime_ms, exec_status)."""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", encoding="utf-8", delete=False
        ) as tf:
            tf.write(code)
            tmp_path = tf.name

        start = time.perf_counter()
        proc = subprocess.run(
            ["python3", tmp_path],
            input=stdin_data,
            text=True,
            capture_output=True,
            timeout=timeout,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "PYTHONIOENCODING": "utf-8"},
        )
        elapsed_ms = round((time.perf_counter() - start) * 1000.0, 2)
        if proc.returncode != 0:
            return proc.stdout, proc.stderr, elapsed_ms, "Runtime Error"
        return proc.stdout, proc.stderr, elapsed_ms, "OK"
    except subprocess.TimeoutExpired as exc:
        elapsed_ms = round(timeout * 1000.0, 2)
        out = exc.stdout.decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        return out, f"Time Limit Exceeded ({timeout:.0f}s limit)", elapsed_ms, "Time Limit Exceeded"
    except Exception as exc:
        return "", f"Execution error: {exc}", 0.0, "Runtime Error"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def prepare_code_for_problem(code: str, problem: Dict[str, Any]) -> str:
    if problem.get("judge_mode") == "driver" and problem.get("test_driver"):
        return code.rstrip() + "\n\n" + problem["test_driver"].lstrip()
    return code


def evaluate_test_cases(
    code: str,
    problem: Dict[str, Any],
    tests: List[Dict[str, str]],
    hide_hidden: bool = False,
    sample_count: int = 0,
) -> Dict[str, Any]:
    full_code = prepare_code_for_problem(code, problem)
    judge_mode = problem.get("judge_mode", "exact")
    results: List[Dict[str, Any]] = []
    passed_count = 0
    total_runtime_ms = 0.0
    overall_status = "Accepted"

    for idx, tc in enumerate(tests):
        tc_input = tc.get("input", "")
        tc_expected = tc.get("output", "")
        stdout, stderr, runtime_ms, exec_status = run_python_code(full_code, tc_input)
        total_runtime_ms += runtime_ms

        if exec_status != "OK":
            passed = False
            case_status = exec_status
        else:
            passed = compare_output(stdout, tc_expected, judge_mode)
            case_status = "Accepted" if passed else "Wrong Answer"

        if passed:
            passed_count += 1
        elif overall_status == "Accepted":
            overall_status = case_status

        is_hidden = hide_hidden and idx >= sample_count
        if is_hidden:
            results.append(
                {
                    "index": idx + 1,
                    "is_hidden": True,
                    "passed": passed,
                    "status": case_status,
                    "runtime_ms": runtime_ms,
                    "stderr": stderr if case_status == "Runtime Error" else "",
                }
            )
        else:
            results.append(
                {
                    "index": idx + 1,
                    "is_hidden": False,
                    "passed": passed,
                    "status": case_status,
                    "input": tc_input,
                    "expected": tc_expected,
                    "actual": stdout,
                    "stderr": stderr,
                    "runtime_ms": runtime_ms,
                }
            )

    avg_runtime = round(total_runtime_ms / len(tests), 2) if tests else 0.0
    return {
        "status": overall_status,
        "passed_count": passed_count,
        "total_count": len(tests),
        "runtime_ms": avg_runtime,
        "results": results,
    }


def make_session_token(user_id: str) -> str:
    secret = os.environ.get("SESSION_SECRET", "col1000-iitd-secret")
    return hashlib.sha256(f"{user_id}:{secret}".encode("utf-8")).hexdigest()[:32]


def verify_google_id_token(credential: str, expected_client_id: str) -> Optional[Dict[str, Any]]:
    url = "https://oauth2.googleapis.com/tokeninfo?" + urllib.parse.urlencode({"id_token": credential})
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=8.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if expected_client_id and data.get("aud") != expected_client_id:
            return None
        if str(data.get("email_verified", "")).lower() != "true":
            return None
        return data
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return None


class COL1000Handler(BaseHTTPRequestHandler):
    server_version = "COL1000Server/1.0"

    def log_message(self, format: str, *args: Any):
        # Clean concise logging
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}")

    def send_json(self, payload: Any, status: int = 200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, file_path: str, content_type: Optional[str] = None):
        if not os.path.isfile(file_path):
            self.send_json({"error": "File not found"}, status=404)
            return
        if not content_type:
            guessed, _ = mimetypes.guess_type(file_path)
            content_type = guessed or "application/octet-stream"
        with open(file_path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_json_body(self) -> Optional[Dict[str, Any]]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return None
        if length <= 0 or length > 2 * 1024 * 1024:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def get_current_user_id(self, query_params: Dict[str, List[str]]) -> Optional[str]:
        uid = self.headers.get("X-User-Id")
        if uid:
            return uid.strip()
        if "user_id" in query_params and query_params["user_id"]:
            return query_params["user_id"][0].strip()
        cookie_hdr = self.headers.get("Cookie")
        if cookie_hdr:
            cookie = SimpleCookie()
            cookie.load(cookie_hdr)
            if "col1000_uid" in cookie:
                return cookie["col1000_uid"].value.strip()
        return None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
            return

        if path.startswith("/static/"):
            rel = path[len("/static/"):]
            safe_path = os.path.normpath(os.path.join(STATIC_DIR, rel))
            if not safe_path.startswith(os.path.abspath(STATIC_DIR)):
                self.send_json({"error": "Forbidden"}, status=403)
                return
            self.send_file(safe_path)
            return

        if path == "/COL1000_Practice_Problems_v2.pdf":
            if not os.path.isfile(PDF_PATH):
                from generate_pdf import build_pdf
                build_pdf(PDF_PATH)
            self.send_file(PDF_PATH, "application/pdf")
            return

        if path == "/api/config":
            self.send_json({"google_client_id": get_google_client_id()})
            return

        if path == "/api/problems":
            uid = self.get_current_user_id(query)
            solved_ids = set()
            if uid:
                conn = get_db()
                try:
                    rows = conn.execute(
                        "SELECT DISTINCT problem_id FROM submissions WHERE user_id = ? AND status = 'Accepted'",
                        (uid,),
                    ).fetchall()
                    solved_ids = {int(r["problem_id"]) for r in rows}
                finally:
                    conn.close()

            summaries = [
                {
                    "id": p["id"],
                    "slug": p["slug"],
                    "title": p["title"],
                    "difficulty": p["difficulty"],
                    "difficulty_tier": p["difficulty_tier"],
                    "judge_mode": p.get("judge_mode", "exact"),
                    "solved": int(p["id"]) in solved_ids,
                }
                for p in PROBLEMS
            ]
            self.send_json({"problems": summaries})
            return

        if path.startswith("/api/problems/"):
            ident = path[len("/api/problems/"):].strip("/")
            prob = None
            if ident.isdigit():
                prob = PROBLEMS_BY_ID.get(int(ident))
            else:
                prob = PROBLEMS_BY_SLUG.get(ident)
            if not prob:
                self.send_json({"error": "Problem not found"}, status=404)
                return

            uid = self.get_current_user_id(query)
            solved = False
            if uid:
                conn = get_db()
                try:
                    row = conn.execute(
                        "SELECT 1 FROM submissions WHERE user_id = ? AND problem_id = ? AND status = 'Accepted' LIMIT 1",
                        (uid, int(prob["id"])),
                    ).fetchone()
                    solved = row is not None
                finally:
                    conn.close()

            safe_prob = {
                "id": prob["id"],
                "slug": prob["slug"],
                "title": prob["title"],
                "difficulty": prob["difficulty"],
                "difficulty_tier": prob["difficulty_tier"],
                "statement": prob["statement"],
                "worked_example": prob.get("worked_example", ""),
                "input_format": prob.get("input_format", ""),
                "output_format": prob.get("output_format", ""),
                "constraints": prob.get("constraints", ""),
                "starter_code": prob.get("starter_code", ""),
                "judge_mode": prob.get("judge_mode", "exact"),
                "sample_tests": prob.get("sample_tests", []),
                "hidden_count": len(prob.get("hidden_tests", [])),
                "hints": prob.get("hints", []),
                "solution_steps": prob.get("solution_steps", []),
                "solution_code": prob.get("solution_code", ""),
                "solved": solved,
            }
            self.send_json(safe_prob)
            return

        if path == "/api/submissions":
            prob_id_str = (query.get("problem_id") or [""])[0]
            uid = self.get_current_user_id(query)
            if not prob_id_str.isdigit() or not uid:
                self.send_json({"submissions": []})
                return
            conn = get_db()
            try:
                rows = conn.execute(
                    """
                    SELECT id, user_id, problem_id, status, passed_count, total_count, runtime_ms, code, created_at
                    FROM submissions
                    WHERE problem_id = ? AND user_id = ?
                    ORDER BY id DESC
                    LIMIT 50
                    """,
                    (int(prob_id_str), uid),
                ).fetchall()
                subs = [dict(r) for r in rows]
            finally:
                conn.close()
            self.send_json({"submissions": subs})
            return

        if path == "/api/leaderboard":
            conn = get_db()
            try:
                users = conn.execute("SELECT id, name, email, avatar FROM users").fetchall()
                accepted_rows = conn.execute(
                    """
                    SELECT user_id, problem_id, MAX(created_at) AS solved_at
                    FROM submissions
                    WHERE status = 'Accepted'
                    GROUP BY user_id, problem_id
                    """
                ).fetchall()
                sub_counts_rows = conn.execute(
                    "SELECT user_id, COUNT(*) AS cnt FROM submissions GROUP BY user_id"
                ).fetchall()
            finally:
                conn.close()

            sub_counts = {r["user_id"]: int(r["cnt"]) for r in sub_counts_rows}
            user_solved: Dict[str, Dict[int, str]] = {}
            for r in accepted_rows:
                user_solved.setdefault(r["user_id"], {})[int(r["problem_id"])] = r["solved_at"]

            board = []
            for u in users:
                uid = u["id"]
                solved_map = user_solved.get(uid, {})
                easy_c = medium_c = hard_c = 0
                last_solved = ""
                for pid, ts in solved_map.items():
                    prob = PROBLEMS_BY_ID.get(pid)
                    if not prob:
                        continue
                    tier = prob.get("difficulty_tier", "Medium")
                    if tier == "Easy":
                        easy_c += 1
                    elif tier == "Hard":
                        hard_c += 1
                    else:
                        medium_c += 1
                    if ts > last_solved:
                        last_solved = ts

                score = easy_c * TIER_POINTS["Easy"] + medium_c * TIER_POINTS["Medium"] + hard_c * TIER_POINTS["Hard"]
                board.append(
                    {
                        "user_id": uid,
                        "name": u["name"],
                        "email": u["email"],
                        "avatar": u["avatar"],
                        "solved_count": len(solved_map),
                        "easy_count": easy_c,
                        "medium_count": medium_c,
                        "hard_count": hard_c,
                        "score": score,
                        "submissions_count": sub_counts.get(uid, 0),
                        "last_solved_at": last_solved,
                    }
                )

            board.sort(
                key=lambda x: (
                    -x["score"],
                    -x["solved_count"],
                    x["last_solved_at"] or "9999",
                    x["name"].lower(),
                )
            )
            for idx, entry in enumerate(board, start=1):
                entry["rank"] = idx

            self.send_json({"leaderboard": board})
            return

        self.send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        data = self.read_json_body()
        if data is None:
            self.send_json({"error": "Invalid JSON body"}, status=400)
            return

        if path == "/api/run":
            prob_id = data.get("problem_id")
            code = data.get("code", "")
            custom_input = data.get("custom_input")

            if prob_id is None or not str(prob_id).isdigit() or int(prob_id) not in PROBLEMS_BY_ID:
                self.send_json({"error": "Invalid problem_id"}, status=400)
                return

            prob = PROBLEMS_BY_ID[int(prob_id)]
            if custom_input is not None:
                full_code = prepare_code_for_problem(code, prob)
                stdout, stderr, runtime_ms, exec_status = run_python_code(full_code, str(custom_input))
                self.send_json(
                    {
                        "mode": "custom",
                        "status": exec_status,
                        "stdout": stdout,
                        "stderr": stderr,
                        "runtime_ms": runtime_ms,
                    }
                )
                return

            samples = prob.get("sample_tests", [])
            eval_res = evaluate_test_cases(code, prob, samples, hide_hidden=False)
            eval_res["mode"] = "samples"
            self.send_json(eval_res)
            return

        if path == "/api/submit":
            prob_id = data.get("problem_id")
            code = data.get("code", "")
            user_id = (data.get("user_id") or self.headers.get("X-User-Id") or "guest").strip()

            if prob_id is None or not str(prob_id).isdigit() or int(prob_id) not in PROBLEMS_BY_ID:
                self.send_json({"error": "Invalid problem_id"}, status=400)
                return

            prob = PROBLEMS_BY_ID[int(prob_id)]
            samples = prob.get("sample_tests", [])
            hidden = prob.get("hidden_tests", [])
            all_tests = samples + hidden

            eval_res = evaluate_test_cases(
                code,
                prob,
                all_tests,
                hide_hidden=True,
                sample_count=len(samples),
            )
            now_iso = datetime.now(timezone.utc).isoformat()
            conn = get_db()
            try:
                cur = conn.execute(
                    """
                    INSERT INTO submissions (user_id, problem_id, status, passed_count, total_count, runtime_ms, code, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        int(prob["id"]),
                        eval_res["status"],
                        eval_res["passed_count"],
                        eval_res["total_count"],
                        eval_res["runtime_ms"],
                        code,
                        now_iso,
                    ),
                )
                sub_id = cur.lastrowid
                conn.commit()
            finally:
                conn.close()

            eval_res["submission_id"] = sub_id
            eval_res["created_at"] = now_iso
            self.send_json(eval_res)
            return

        if path == "/api/config":
            cid = str(data.get("google_client_id", "")).strip()
            if cid and not cid.endswith(".apps.googleusercontent.com"):
                self.send_json({"error": "Client ID should end with .apps.googleusercontent.com"}, status=400)
                return
            save_google_client_id(cid)
            self.send_json({"google_client_id": cid})
            return

        if path == "/api/auth/google":
            google_client_id = get_google_client_id()
            credential = data.get("credential")
            is_demo = bool(data.get("demo"))

            if credential and google_client_id:
                info = verify_google_id_token(credential, google_client_id)
                if not info:
                    self.send_json({"error": "Invalid Google ID token"}, status=401)
                    return
                uid = f"google_{info['sub']}"
                name = info.get("name") or info.get("email", "IITD Student").split("@")[0]
                email = info.get("email", "")
                avatar = info.get("picture", "")
                demo_flag = 0
            elif is_demo or not google_client_id:
                name = (data.get("name") or "").strip()
                email = (data.get("email") or "").strip().lower()
                if not name or not email or "@" not in email:
                    self.send_json({"error": "Valid name and email are required for Demo Sign-In"}, status=400)
                    return
                uid_hash = hashlib.sha256(email.encode("utf-8")).hexdigest()[:12]
                uid = f"iitd_{uid_hash}"
                initials = "".join(p[0].upper() for p in re.split(r"\s+", name) if p)[:2] or "ST"
                avatar = initials
                demo_flag = 1
            else:
                self.send_json({"error": "Google credential required"}, status=400)
                return

            now_iso = datetime.now(timezone.utc).isoformat()
            conn = get_db()
            try:
                existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
                if existing:
                    uid = existing["id"]
                    conn.execute(
                        "UPDATE users SET name = ?, avatar = ?, is_demo = ? WHERE id = ?",
                        (name, avatar, demo_flag, uid),
                    )
                else:
                    conn.execute(
                        "INSERT INTO users (id, name, email, avatar, is_demo, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (uid, name, email, avatar, demo_flag, now_iso),
                    )
                conn.commit()
            finally:
                conn.close()

            user_obj = {
                "id": uid,
                "name": name,
                "email": email,
                "avatar": avatar,
                "is_demo": bool(demo_flag),
            }
            self.send_json({"user": user_obj, "session_token": make_session_token(uid)})
            return

        self.send_json({"error": "Not found"}, status=404)


def run_server():
    init_db()
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), COL1000Handler)
    print(f"COL1000 Practice Platform running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()


if __name__ == "__main__":
    run_server()
