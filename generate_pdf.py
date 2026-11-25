#!/usr/bin/env python3
"""Pure-Python PDF 1.4 generator for IIT Delhi COL1000 Practice Problems."""

import os
import textwrap
import zlib
from typing import List, Tuple

from problems_data import PROBLEMS

PAGE_WIDTH = 595.28   # A4 width in points
PAGE_HEIGHT = 841.89  # A4 height in points
MARGIN_LEFT = 50
MARGIN_RIGHT = 50
MARGIN_TOP = 54
MARGIN_BOTTOM = 52
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT


def sanitize_pdf_text(text: str) -> str:
    """Convert Unicode characters to clean ASCII/WinAnsi-safe equivalents."""
    if text is None:
        return ""
    replacements = {
        "\u2014": "--",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u2022": "*",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2260": "!=",
        "\u00d7": "x",
        "\u00f7": "/",
        "\u00b2": "^2",
        "\u00b3": "^3",
        "\u2212": "-",
        "\u00a0": " ",
        "\t": "    ",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Encode/decode latin-1 replacing any remaining unsupported chars
    return text.encode("latin-1", errors="replace").decode("latin-1")


def escape_pdf_literal(text: str) -> str:
    """Escape special characters for PDF literal strings (...)."""
    return (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


class PDFCanvas:
    """Builds multi-page PDF 1.4 documents using standard Type1 fonts."""

    def __init__(self):
        self.pages: List[List[str]] = []
        self.current_ops: List[str] = []
        self.y = PAGE_HEIGHT - MARGIN_TOP
        self._new_page()

    def _new_page(self):
        if self.current_ops:
            self.pages.append(self.current_ops)
        self.current_ops = []
        self.y = PAGE_HEIGHT - MARGIN_TOP

    def ensure_space(self, needed_height: float):
        if self.y - needed_height < MARGIN_BOTTOM:
            self._new_page()

    def draw_rect(self, x: float, y: float, w: float, h: float, fill_rgb: Tuple[float, float, float]):
        r, g, b = fill_rgb
        self.current_ops.append(f"q {r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {y:.2f} {w:.2f} {h:.2f} re f Q")

    def draw_line(self, x1: float, y1: float, x2: float, y2: float, rgb: Tuple[float, float, float] = (0.82, 0.84, 0.88), width: float = 0.7):
        r, g, b = rgb
        self.current_ops.append(f"q {r:.3f} {g:.3f} {b:.3f} RG {width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S Q")

    def draw_text_line(
        self,
        text: str,
        x: float,
        y: float,
        font: str = "F1",
        size: float = 10.0,
        rgb: Tuple[float, float, float] = (0.12, 0.14, 0.18),
    ):
        safe = escape_pdf_literal(sanitize_pdf_text(text))
        r, g, b = rgb
        self.current_ops.append(
            f"BT /{font} {size:.1f} Tf {r:.3f} {g:.3f} {b:.3f} rg {x:.2f} {y:.2f} Td ({safe}) Tj ET"
        )

    def add_spacer(self, pts: float = 6.0):
        self.y -= pts

    def add_wrapped_paragraph(
        self,
        text: str,
        font: str = "F1",
        size: float = 9.8,
        line_height: float = 13.5,
        indent: float = 0.0,
        rgb: Tuple[float, float, float] = (0.15, 0.17, 0.21),
    ):
        clean = sanitize_pdf_text(text)
        # Approximate chars per line based on font
        avg_char_w = size * (0.58 if font in ("F3", "F4") else 0.49)
        max_chars = max(20, int((CONTENT_WIDTH - indent) / avg_char_w))

        for raw_para in clean.splitlines():
            stripped = raw_para.rstrip()
            if not stripped:
                self.add_spacer(line_height * 0.55)
                continue
            wrapped = textwrap.wrap(
                stripped,
                width=max_chars,
                break_long_words=True,
                break_on_hyphens=False,
            ) or [""]
            for line in wrapped:
                self.ensure_space(line_height)
                self.draw_text_line(line, MARGIN_LEFT + indent, self.y, font=font, size=size, rgb=rgb)
                self.y -= line_height

    def add_code_block(
        self,
        code: str,
        font: str = "F3",
        size: float = 8.6,
        line_height: float = 11.8,
        bg_rgb: Tuple[float, float, float] = (0.95, 0.96, 0.98),
        text_rgb: Tuple[float, float, float] = (0.10, 0.12, 0.16),
    ):
        clean = sanitize_pdf_text(code).rstrip("\n")
        if not clean:
            clean = "(empty)"
        avg_char_w = size * 0.60
        max_chars = max(30, int((CONTENT_WIDTH - 16) / avg_char_w))

        lines: List[str] = []
        for raw_line in clean.splitlines():
            if len(raw_line) <= max_chars:
                lines.append(raw_line)
            else:
                for i in range(0, len(raw_line), max_chars):
                    lines.append(raw_line[i : i + max_chars])

        # Draw line-by-line with subtle background strip so blocks can span pages cleanly
        for idx, line in enumerate(lines):
            self.ensure_space(line_height + 2)
            self.draw_rect(
                MARGIN_LEFT + 4,
                self.y - 3,
                CONTENT_WIDTH - 8,
                line_height,
                bg_rgb,
            )
            self.draw_text_line(line, MARGIN_LEFT + 10, self.y, font=font, size=size, rgb=text_rgb)
            self.y -= line_height
        self.add_spacer(4)

    def add_section_heading(self, title: str):
        self.ensure_space(22)
        self.add_spacer(4)
        self.draw_text_line(title, MARGIN_LEFT, self.y, font="F2", size=10.5, rgb=(0.12, 0.25, 0.48))
        self.y -= 14

    def finalize_pages(self) -> List[bytes]:
        if self.current_ops:
            self.pages.append(self.current_ops)
            self.current_ops = []

        total = len(self.pages)
        encoded_pages: List[bytes] = []
        for idx, ops in enumerate(self.pages, start=1):
            footer_ops = [
                f"q 0.85 0.87 0.90 RG 0.6 w {MARGIN_LEFT} 36 m {PAGE_WIDTH - MARGIN_RIGHT} 36 l S Q",
                f"BT /F1 8.5 Tf 0.45 0.48 0.54 rg {MARGIN_LEFT} 24 Td (IIT Delhi COL1000 -- Practice Problem Set) Tj ET",
                f"BT /F1 8.5 Tf 0.45 0.48 0.54 rg {PAGE_WIDTH - MARGIN_RIGHT - 65:.2f} 24 Td (Page {idx} of {total}) Tj ET",
            ]
            stream_str = "\n".join(ops + footer_ops) + "\n"
            encoded_pages.append(stream_str.encode("latin-1", errors="replace"))
        return encoded_pages

    def write_pdf(self, output_path: str):
        page_streams = self.finalize_pages()
        objects: List[bytes] = []

        def add_obj(body: bytes) -> int:
            objects.append(body)
            return len(objects)

        # 1: Catalog, 2: Pages (placeholders updated after pages are added)
        catalog_id = add_obj(b"")
        pages_id = add_obj(b"")

        # Fonts: F1=Helvetica, F2=Helvetica-Bold, F3=Courier, F4=Courier-Bold
        f1_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        f2_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        f3_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")
        f4_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold /Encoding /WinAnsiEncoding >>")

        font_dict = f"<< /F1 {f1_id} 0 R /F2 {f2_id} 0 R /F3 {f3_id} 0 R /F4 {f4_id} 0 R >>".encode("ascii")

        page_ids: List[int] = []
        for raw_stream in page_streams:
            compressed = zlib.compress(raw_stream, level=6)
            stream_obj = (
                f"<< /Length {len(compressed)} /Filter /FlateDecode >>\nstream\n".encode("ascii")
                + compressed
                + b"\nendstream"
            )
            content_id = add_obj(stream_obj)
            page_obj = (
                f"<< /Type /Page /Parent {pages_id} 0 R "
                f"/MediaBox [0 0 {PAGE_WIDTH:.2f} {PAGE_HEIGHT:.2f}] "
                f"/Resources << /Font {font_dict.decode('ascii')} >> "
                f"/Contents {content_id} 0 R >>"
            ).encode("ascii")
            page_id = add_obj(page_obj)
            page_ids.append(page_id)

        kids_str = " ".join(f"{pid} 0 R" for pid in page_ids)
        objects[catalog_id - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii")
        objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_ids)} >>".encode("ascii")

        # Assemble PDF bytes with xref
        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets: List[int] = [0]
        for idx, body in enumerate(objects, start=1):
            offsets.append(len(out))
            out.extend(f"{idx} 0 obj\n".encode("ascii"))
            out.extend(body)
            out.extend(b"\nendobj\n")

        xref_offset = len(out)
        out.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        out.extend(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            out.extend(f"{off:010d} 00000 n \n".encode("ascii"))

        out.extend(
            (
                f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
                f"startxref\n{xref_offset}\n%%EOF\n"
            ).encode("ascii")
        )

        with open(output_path, "wb") as f:
            f.write(out)


def difficulty_color(tier: str) -> Tuple[float, float, float]:
    t = (tier or "").lower()
    if t == "easy":
        return (0.06, 0.55, 0.36)
    if t == "medium":
        return (0.76, 0.45, 0.04)
    return (0.78, 0.14, 0.24)


def build_pdf(output_path: str = "COL1000_Practice_Problems_v2.pdf"):
    pdf = PDFCanvas()

    # Title Banner on Page 1
    pdf.draw_rect(MARGIN_LEFT, pdf.y - 44, CONTENT_WIDTH, 56, (0.09, 0.14, 0.24))
    pdf.draw_text_line(
        "IIT DELHI -- COL1000: INTRODUCTION TO COMPUTER SCIENCE",
        MARGIN_LEFT + 14,
        pdf.y - 12,
        font="F2",
        size=13.0,
        rgb=(0.98, 0.99, 1.00),
    )
    pdf.draw_text_line(
        f"LeetCode-Style Practice Problem Set ({len(PROBLEMS)} Problems)",
        MARGIN_LEFT + 14,
        pdf.y - 30,
        font="F1",
        size=10.5,
        rgb=(0.75, 0.83, 0.95),
    )
    pdf.y -= 64

    # Compact Table of Contents
    pdf.draw_text_line("Problem Index", MARGIN_LEFT, pdf.y, font="F2", size=11.0, rgb=(0.12, 0.25, 0.48))
    pdf.y -= 15
    for prob in PROBLEMS:
        pdf.ensure_space(13)
        tier = prob.get("difficulty_tier", "Medium")
        pid = prob.get("id")
        title = prob.get("title", "")
        pdf.draw_text_line(f"{pid:2d}. {title}", MARGIN_LEFT + 8, pdf.y, font="F1", size=9.2, rgb=(0.15, 0.17, 0.21))
        pdf.draw_text_line(f"[{tier}]", PAGE_WIDTH - MARGIN_RIGHT - 55, pdf.y, font="F2", size=8.8, rgb=difficulty_color(tier))
        pdf.y -= 12.5

    # Each Problem
    for idx, prob in enumerate(PROBLEMS):
        if idx > 0 or pdf.y < PAGE_HEIGHT * 0.45:
            pdf._new_page()
        else:
            pdf.add_spacer(14)

        pid = prob.get("id")
        title = prob.get("title", "")
        tier = prob.get("difficulty_tier", "Medium")
        diff_label = prob.get("difficulty", tier)

        # Problem Header Box
        pdf.ensure_space(46)
        pdf.draw_rect(MARGIN_LEFT, pdf.y - 24, CONTENT_WIDTH, 32, (0.93, 0.95, 0.98))
        pdf.draw_line(MARGIN_LEFT, pdf.y - 24, MARGIN_LEFT + CONTENT_WIDTH, pdf.y - 24, rgb=(0.72, 0.78, 0.88), width=1.0)
        pdf.draw_text_line(
            f"Problem {pid}: {title}",
            MARGIN_LEFT + 10,
            pdf.y - 11,
            font="F2",
            size=12.0,
            rgb=(0.08, 0.12, 0.20),
        )
        pdf.draw_text_line(
            f"{tier}" if str(diff_label) == str(tier) else f"{tier} ({diff_label})",
            PAGE_WIDTH - MARGIN_RIGHT - 95,
            pdf.y - 11,
            font="F2",
            size=9.5,
            rgb=difficulty_color(tier),
        )
        pdf.y -= 36

        pdf.add_section_heading("Problem Statement")
        pdf.add_wrapped_paragraph(prob.get("statement", ""))

        if prob.get("worked_example"):
            pdf.add_section_heading("Worked Example")
            pdf.add_wrapped_paragraph(prob["worked_example"], size=9.4, line_height=13.0)

        if prob.get("input_format"):
            pdf.add_section_heading("Input Format")
            pdf.add_wrapped_paragraph(prob["input_format"])

        if prob.get("output_format"):
            pdf.add_section_heading("Output Format")
            pdf.add_wrapped_paragraph(prob["output_format"])

        if prob.get("constraints"):
            pdf.add_section_heading("Constraints")
            pdf.add_wrapped_paragraph(prob["constraints"], font="F3", size=9.0, line_height=12.5)

        if prob.get("starter_code"):
            pdf.add_section_heading("Starter Code (Python 3)")
            pdf.add_code_block(prob["starter_code"])

        samples = prob.get("sample_tests", [])
        if samples:
            pdf.add_section_heading("Sample Test Cases")
            for s_idx, sample in enumerate(samples, start=1):
                pdf.ensure_space(36)
                pdf.draw_text_line(f"Sample {s_idx} Input:", MARGIN_LEFT + 4, pdf.y, font="F2", size=9.2, rgb=(0.22, 0.25, 0.30))
                pdf.y -= 12
                pdf.add_code_block(sample.get("input", ""))
                pdf.ensure_space(28)
                pdf.draw_text_line(f"Sample {s_idx} Output:", MARGIN_LEFT + 4, pdf.y, font="F2", size=9.2, rgb=(0.22, 0.25, 0.30))
                pdf.y -= 12
                pdf.add_code_block(sample.get("output", ""))

    pdf.write_pdf(output_path)
    print(f"Generated {output_path} ({len(PROBLEMS)} problems, {len(pdf.pages)} pages)")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    build_pdf(os.path.join(out_dir, "COL1000_Practice_Problems_v2.pdf"))
