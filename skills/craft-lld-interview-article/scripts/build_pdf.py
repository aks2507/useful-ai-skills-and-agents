#!/usr/bin/env python3
"""Build a self-contained LLD PDF from Markdown and a runnable solution tree."""

from __future__ import annotations

import argparse
import hashlib
import html
import math
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    Flowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


CODE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".h", ".hpp", ".java", ".js",
    ".json", ".kt", ".kts", ".py", ".rb", ".rs", ".swift", ".toml",
    ".ts", ".xml", ".yaml", ".yml",
}
BUILD_FILENAMES = {
    "CMakeLists.txt", "Makefile", "README.md", "build.gradle", "gradlew",
    "gradlew.bat", "package-lock.json", "package.json", "pom.xml",
    "pyproject.toml", "requirements.txt", "settings.gradle", "tsconfig.json",
}
IGNORED_PARTS = {
    ".git", ".idea", ".pytest_cache", ".venv", "__pycache__", "build",
    "dist", "node_modules", "out", "target", "venv",
}

INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#5B6472")
BLUE = colors.HexColor("#315CF5")
PALE_BLUE = colors.HexColor("#EEF3FF")
PALE_GRAY = colors.HexColor("#F5F7FA")
LINE = colors.HexColor("#D8DEE9")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path, help="Final question[-level].md")
    parser.add_argument("--solution-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Defaults to the Markdown stem.pdf")
    parser.add_argument("--author", default="Craft LLD Interview Article")
    return parser.parse_args()


def register_fonts() -> tuple[str, str]:
    candidates = [
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "ArialLocal"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuLocal"),
    ]
    mono_candidates = [
        ("/System/Library/Fonts/Menlo.ttc", "MenloLocal"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "DejaVuMonoLocal"),
    ]
    body = "Helvetica"
    mono = "Courier"
    for path, name in candidates:
        if Path(path).is_file():
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                body = name
                break
            except Exception:
                pass
    for path, name in mono_candidates:
        if Path(path).is_file():
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                mono = name
                break
            except Exception:
                pass
    return body, mono


def styles(body_font: str, mono_font: str) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "LLDTitle", parent=base["Title"], fontName=body_font,
            fontSize=25, leading=30, textColor=INK, spaceAfter=12 * mm,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "LLDH1", parent=base["Heading1"], fontName=body_font,
            fontSize=18, leading=22, textColor=INK, spaceBefore=7 * mm,
            spaceAfter=3 * mm, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "LLDH2", parent=base["Heading2"], fontName=body_font,
            fontSize=14, leading=18, textColor=BLUE, spaceBefore=5 * mm,
            spaceAfter=2 * mm, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "LLDH3", parent=base["Heading3"], fontName=body_font,
            fontSize=11.5, leading=15, textColor=INK, spaceBefore=4 * mm,
            spaceAfter=1.5 * mm, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "LLDBody", parent=base["BodyText"], fontName=body_font,
            fontSize=9.4, leading=13.2, textColor=INK, spaceAfter=2.4 * mm,
        ),
        "small": ParagraphStyle(
            "LLDSmall", parent=base["BodyText"], fontName=body_font,
            fontSize=7.7, leading=10.2, textColor=MUTED,
        ),
        "quote": ParagraphStyle(
            "LLDQuote", parent=base["BodyText"], fontName=body_font,
            fontSize=9.2, leading=13, textColor=INK, leftIndent=4 * mm,
            rightIndent=3 * mm, spaceAfter=2 * mm,
        ),
        "code": ParagraphStyle(
            "LLDCode", fontName=mono_font, fontSize=6.7, leading=8.5,
            textColor=INK, leftIndent=2.5 * mm, rightIndent=2.5 * mm,
            spaceBefore=1.5 * mm, spaceAfter=2.5 * mm,
            backColor=PALE_GRAY, borderColor=LINE, borderWidth=0.4,
            borderPadding=2 * mm,
        ),
        "appendix_code": ParagraphStyle(
            "LLDAppendixCode", fontName=mono_font, fontSize=5.9, leading=7.3,
            textColor=INK, leftIndent=1.5 * mm, rightIndent=1.5 * mm,
            spaceAfter=2 * mm, backColor=PALE_GRAY, borderColor=LINE,
            borderWidth=0.35, borderPadding=1.4 * mm,
        ),
        "appendix_path": ParagraphStyle(
            "LLDAppendixPath", parent=base["Heading2"], fontName=body_font,
            fontSize=9.5, leading=12.5, textColor=BLUE, spaceBefore=4 * mm,
            spaceAfter=2 * mm, keepWithNext=True,
        ),
        "table": ParagraphStyle(
            "LLDTable", parent=base["BodyText"], fontName=body_font,
            fontSize=7.6, leading=10, textColor=INK,
        ),
    }


def inline_markup(value: str, mono_font: str) -> str:
    value = html.escape(value.strip())
    value = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<link href="\2" color="#315CF5">\1</link>',
        value,
    )
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(
        r"`([^`]+)`", rf'<font name="{mono_font}" backColor="#EEF1F5">\1</font>', value
    )
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    value = value.replace("  ", " ")
    return value


def table_rows(lines: list[str], start: int) -> tuple[list[list[str]], int] | None:
    if start + 1 >= len(lines) or "|" not in lines[start]:
        return None
    separator = lines[start + 1].strip()
    cells = [cell.strip() for cell in separator.strip("|").split("|")]
    if not cells or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
        return None
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and "|" in lines[index] and lines[index].strip():
        rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
        index += 1
    del rows[1]
    return rows, index


def add_code(story: list[Flowable], text: str, style: ParagraphStyle, width: int) -> None:
    lines = text.splitlines() or [""]
    for offset in range(0, len(lines), 50):
        chunk = "\n".join(lines[offset : offset + 50])
        story.append(
            Preformatted(
                chunk,
                style,
                maxLineLength=width,
                splitChars=" ".join([".", ",", ":", ";", " "]),
                newLineChars=" ↳ ",
            )
        )


class ClassDiagram(Flowable):
    def __init__(self, source: str, body_font: str, mono_font: str) -> None:
        super().__init__()
        self.source = source
        self.body_font = body_font
        self.mono_font = mono_font
        self.classes, self.relations = self._parse(source)
        self.positions: dict[str, tuple[float, float, float, float]] = {}

    @staticmethod
    def _parse(source: str) -> tuple[OrderedDict[str, list[str]], list[tuple[str, str, str]]]:
        classes: OrderedDict[str, list[str]] = OrderedDict()
        relations: list[tuple[str, str, str]] = []
        current: str | None = None
        relation_re = re.compile(
            r'^\s*([A-Za-z_]\w*)\s+(?:"[^"]+"\s+)?[<>|o*.\-]+\s+'
            r'(?:"[^"]+"\s+)?([A-Za-z_]\w*)(?:\s*:\s*(.+))?$'
        )
        for raw in source.splitlines()[1:]:
            line = raw.strip()
            if not line or line.startswith("%%"):
                continue
            if current is not None:
                if line == "}":
                    current = None
                else:
                    classes[current].append(line)
                continue
            block = re.match(r"class\s+([A-Za-z_]\w*)\s*\{", line)
            if block:
                current = block.group(1)
                classes.setdefault(current, [])
                continue
            plain = re.match(r"class\s+([A-Za-z_]\w*)\b", line)
            if plain:
                classes.setdefault(plain.group(1), [])
                continue
            relation = relation_re.match(line)
            if relation:
                left, right, label = relation.groups()
                classes.setdefault(left, [])
                classes.setdefault(right, [])
                relations.append((left, right, label or ""))
        return classes, relations

    def wrap(self, avail_width: float, _avail_height: float) -> tuple[float, float]:
        self.width = min(avail_width, 175 * mm)
        columns = 2 if len(self.classes) > 1 else 1
        gap = 10 * mm
        box_width = (self.width - gap * (columns - 1)) / columns
        row_heights: list[float] = []
        items = list(self.classes.items())
        for start in range(0, len(items), columns):
            heights = [15 * mm + min(len(members), 7) * 3.8 * mm for _, members in items[start:start + columns]]
            row_heights.append(max(heights, default=15 * mm))
        self.legend_height = (5 + len(self.relations) * 3.5) * mm if self.relations else 0
        total = sum(row_heights) + max(0, len(row_heights) - 1) * 10 * mm + 4 * mm + self.legend_height
        self.height = max(total, 25 * mm)
        self.positions.clear()
        y_top = self.height - 2 * mm
        item_index = 0
        for row_height in row_heights:
            for column in range(columns):
                if item_index >= len(items):
                    break
                name, members = items[item_index]
                actual_height = 15 * mm + min(len(members), 7) * 3.8 * mm
                x = column * (box_width + gap)
                y = y_top - actual_height
                self.positions[name] = (x, y, box_width, actual_height)
                item_index += 1
            y_top -= row_height + 10 * mm
        return self.width, self.height

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.8)
        for left, right, label in self.relations:
            if left not in self.positions or right not in self.positions:
                continue
            lx, ly, lw, lh = self.positions[left]
            rx, ry, rw, rh = self.positions[right]
            left_center = (lx + lw / 2, ly + lh / 2)
            right_center = (rx + rw / 2, ry + rh / 2)
            x1, y1 = self._edge_point((lx, ly, lw, lh), right_center)
            x2, y2 = self._edge_point((rx, ry, rw, rh), left_center)
            canvas.line(x1, y1, x2, y2)
            angle = math.atan2(y2 - y1, x2 - x1)
            size = 3.5
            canvas.line(x2, y2, x2 - size * math.cos(angle - 0.5), y2 - size * math.sin(angle - 0.5))
            canvas.line(x2, y2, x2 - size * math.cos(angle + 0.5), y2 - size * math.sin(angle + 0.5))
        for name, members in self.classes.items():
            x, y, width, height = self.positions[name]
            header = 8 * mm
            canvas.setFillColor(PALE_BLUE)
            canvas.setStrokeColor(BLUE)
            canvas.roundRect(x, y, width, height, 2.5 * mm, fill=1, stroke=1)
            canvas.setFillColor(BLUE)
            canvas.roundRect(x, y + height - header, width, header, 2.5 * mm, fill=1, stroke=0)
            canvas.setFillColor(colors.white)
            canvas.setFont(self.body_font, 8.2)
            canvas.drawCentredString(x + width / 2, y + height - 5.3 * mm, name)
            canvas.setFillColor(INK)
            canvas.setFont(self.mono_font, 6.2)
            text_y = y + height - header - 4.5 * mm
            for member in members[:7]:
                display = member if len(member) <= 48 else member[:45] + "..."
                canvas.drawString(x + 3 * mm, text_y, display)
                text_y -= 3.8 * mm
        if self.relations:
            canvas.setFillColor(MUTED)
            canvas.setFont(self.body_font, 5.8)
            canvas.drawString(0, self.legend_height - 3 * mm, "Relationships")
            for index, (left, right, label) in enumerate(self.relations):
                suffix = f": {label}" if label else ""
                canvas.drawString(3 * mm, self.legend_height - (6.5 + index * 3.5) * mm, f"{left} → {right}{suffix}")
        canvas.restoreState()

    @staticmethod
    def _edge_point(box: tuple[float, float, float, float], target: tuple[float, float]) -> tuple[float, float]:
        x, y, width, height = box
        center_x, center_y = x + width / 2, y + height / 2
        dx, dy = target[0] - center_x, target[1] - center_y
        if dx == 0 and dy == 0:
            return center_x, center_y
        x_scale = (width / 2) / abs(dx) if dx else float("inf")
        y_scale = (height / 2) / abs(dy) if dy else float("inf")
        scale = min(x_scale, y_scale)
        return center_x + dx * scale, center_y + dy * scale


class StateDiagram(Flowable):
    def __init__(self, source: str, body_font: str) -> None:
        super().__init__()
        self.body_font = body_font
        self.transitions = self._parse(source)
        self.nodes = list(OrderedDict.fromkeys(n for edge in self.transitions for n in edge[:2] if n not in {"[*]"}))
        self.positions: dict[str, tuple[float, float]] = {}

    @staticmethod
    def _parse(source: str) -> list[tuple[str, str, str]]:
        transitions = []
        for line in source.splitlines()[1:]:
            match = re.match(r"\s*(\[\*\]|[\w.]+)\s*-->\s*(\[\*\]|[\w.]+)(?:\s*:\s*(.+))?", line)
            if match:
                transitions.append((match.group(1), match.group(2), match.group(3) or ""))
        return transitions

    def wrap(self, avail_width: float, _avail_height: float) -> tuple[float, float]:
        self.width = min(avail_width, 175 * mm)
        if len(self.nodes) <= 4:
            self.height = 42 * mm
            node_y = self.height / 2
            for index, name in enumerate(self.nodes):
                self.positions[name] = ((index + 0.5) * self.width / max(1, len(self.nodes)), node_y)
            return self.width, self.height
        rows = max(1, math.ceil(len(self.nodes) / 2))
        self.height = rows * 24 * mm
        self.positions.clear()
        for index, name in enumerate(self.nodes):
            col, row = index % 2, index // 2
            x = (0.25 + col * 0.5) * self.width
            y = self.height - (row + 0.55) * 24 * mm
            self.positions[name] = (x, y)
        return self.width, self.height

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        normal_edges = [edge for edge in self.transitions if "[*]" not in edge[:2] and edge[0] != edge[1]]
        grouped: dict[frozenset[str], list[tuple[str, str, str]]] = {}
        for edge in normal_edges:
            grouped.setdefault(frozenset(edge[:2]), []).append(edge)
        for edges in grouped.values():
            for index, (left, right, label) in enumerate(edges):
                if left not in self.positions or right not in self.positions:
                    continue
                x1, y1 = self.positions[left]
                x2, y2 = self.positions[right]
                direction = 1 if x2 >= x1 else -1
                x1 += direction * 27 * mm
                x2 -= direction * 27 * mm
                offset = (index - (len(edges) - 1) / 2) * 7 * mm
                route_y = (y1 + y2) / 2 + offset
                canvas.setStrokeColor(LINE)
                canvas.line(x1, y1, x1 + direction * 3 * mm, route_y)
                canvas.line(x1 + direction * 3 * mm, route_y, x2 - direction * 3 * mm, route_y)
                canvas.line(x2 - direction * 3 * mm, route_y, x2, y2)
                self._arrow(canvas, x2 - direction * 3 * mm, route_y, x2, y2)
                if label:
                    canvas.setFont(self.body_font, 5.8)
                    canvas.setFillColor(MUTED)
                    canvas.drawCentredString((x1 + x2) / 2, route_y + 3, label[:38])
        for left, right, label in self.transitions:
            if left == "[*]" and right in self.positions:
                x2, y2 = self.positions[right]
                x1, y1 = x2, y2 + 14 * mm
                canvas.setFillColor(INK)
                canvas.circle(x1, y1, 2.2, fill=1, stroke=0)
                canvas.setStrokeColor(LINE)
                canvas.line(x1, y1 - 2.2, x2, y2 + 5 * mm)
                self._arrow(canvas, x1, y1 - 2.2, x2, y2 + 5 * mm)
            elif right == "[*]" and left in self.positions:
                x1, y1 = self.positions[left]
                x2, y2 = x1, y1 - 14 * mm
                canvas.setStrokeColor(LINE)
                canvas.line(x1, y1 - 5 * mm, x2, y2 + 2.2)
                canvas.setFillColor(colors.white)
                canvas.circle(x2, y2, 3.2, fill=1, stroke=1)
                canvas.setFillColor(INK)
                canvas.circle(x2, y2, 1.7, fill=1, stroke=0)
            elif left == right and left in self.positions:
                x, y = self.positions[left]
                canvas.setStrokeColor(LINE)
                canvas.bezier(x + 10 * mm, y + 5 * mm, x + 30 * mm, y + 18 * mm, x - 30 * mm, y + 18 * mm, x - 10 * mm, y + 5 * mm)
                self._arrow(canvas, x - 18 * mm, y + 12 * mm, x - 10 * mm, y + 5 * mm)
                if label:
                    canvas.setFont(self.body_font, 5.8)
                    canvas.setFillColor(MUTED)
                    canvas.drawCentredString(x, y + 15 * mm, label[:38])
        for name, (x, y) in self.positions.items():
            width, height = 54 * mm, 10 * mm
            canvas.setFillColor(PALE_BLUE)
            canvas.setStrokeColor(BLUE)
            canvas.roundRect(x - width / 2, y - height / 2, width, height, 3 * mm, fill=1, stroke=1)
            canvas.setFillColor(INK)
            canvas.setFont(self.body_font, 8)
            canvas.drawCentredString(x, y - 2.5, name)
        canvas.restoreState()

    @staticmethod
    def _arrow(canvas, x1: float, y1: float, x2: float, y2: float) -> None:  # type: ignore[no-untyped-def]
        angle = math.atan2(y2 - y1, x2 - x1)
        size = 3.5
        canvas.line(x2, y2, x2 - size * math.cos(angle - 0.5), y2 - size * math.sin(angle - 0.5))
        canvas.line(x2, y2, x2 - size * math.cos(angle + 0.5), y2 - size * math.sin(angle + 0.5))


class SequenceDiagram(Flowable):
    def __init__(self, source: str, body_font: str) -> None:
        super().__init__()
        self.body_font = body_font
        self.participants, self.messages = self._parse(source)
        self.x_positions: dict[str, float] = {}

    @staticmethod
    def _parse(source: str) -> tuple[OrderedDict[str, str], list[tuple[str, str, str]]]:
        participants: OrderedDict[str, str] = OrderedDict()
        messages: list[tuple[str, str, str]] = []
        for raw in source.splitlines()[1:]:
            line = raw.strip()
            participant = re.match(r"(?:actor|participant)\s+(\w+)(?:\s+as\s+(.+))?", line)
            if participant:
                participants[participant.group(1)] = participant.group(2) or participant.group(1)
                continue
            message = re.match(r"(\w+)\s*-+>>?\s*(\w+)\s*:\s*(.+)", line)
            if message:
                left, right, label = message.groups()
                participants.setdefault(left, left)
                participants.setdefault(right, right)
                messages.append((left, right, label))
        return participants, messages

    def wrap(self, avail_width: float, _avail_height: float) -> tuple[float, float]:
        self.width = min(avail_width, 175 * mm)
        self.height = 22 * mm + max(1, len(self.messages)) * 12 * mm
        count = max(1, len(self.participants))
        for index, name in enumerate(self.participants):
            self.x_positions[name] = (index + 0.5) * self.width / count
        return self.width, self.height

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        bottom = 4 * mm
        top = self.height - 9 * mm
        for name, label in self.participants.items():
            x = self.x_positions[name]
            canvas.setFillColor(PALE_BLUE)
            canvas.setStrokeColor(BLUE)
            canvas.roundRect(x - 17 * mm, top, 34 * mm, 8 * mm, 2 * mm, fill=1, stroke=1)
            canvas.setFillColor(INK)
            canvas.setFont(self.body_font, 7)
            canvas.drawCentredString(x, top + 2.7 * mm, label[:24])
            canvas.setStrokeColor(LINE)
            canvas.setDash(2, 2)
            canvas.line(x, top, x, bottom)
            canvas.setDash()
        for index, (left, right, label) in enumerate(self.messages):
            y = top - (index + 1) * 11 * mm
            x1, x2 = self.x_positions[left], self.x_positions[right]
            canvas.setStrokeColor(INK)
            canvas.line(x1, y, x2, y)
            direction = 1 if x2 >= x1 else -1
            canvas.line(x2, y, x2 - direction * 4, y + 2.5)
            canvas.line(x2, y, x2 - direction * 4, y - 2.5)
            canvas.setFont(self.body_font, 6.2)
            canvas.setFillColor(MUTED)
            canvas.drawCentredString((x1 + x2) / 2, y + 3.5, label[:58])
        canvas.restoreState()


def diagram_flowable(source: str, body_font: str, mono_font: str) -> Flowable | None:
    first = next((line.strip() for line in source.splitlines() if line.strip()), "")
    if first == "classDiagram":
        diagram = ClassDiagram(source, body_font, mono_font)
        return diagram if diagram.classes else None
    if first.startswith("stateDiagram"):
        diagram = StateDiagram(source, body_font)
        return diagram if diagram.transitions else None
    if first == "sequenceDiagram":
        diagram = SequenceDiagram(source, body_font)
        return diagram if diagram.participants and diagram.messages else None
    return None


def markdown_story(markdown: str, style: dict[str, ParagraphStyle], body_font: str, mono_font: str) -> tuple[list[Flowable], list[str]]:
    story: list[Flowable] = []
    warnings: list[str] = []
    lines = markdown.splitlines()
    index = 0
    first_heading = True
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        fence = re.match(r"^```\s*([^\s]*)", line)
        if fence:
            language = fence.group(1).lower()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            code = "\n".join(code_lines)
            if language == "mermaid":
                diagram = diagram_flowable(code, body_font, mono_font)
                if diagram is not None:
                    story.extend([Spacer(1, 2 * mm), diagram, Spacer(1, 3 * mm)])
                else:
                    warnings.append("Unsupported Mermaid syntax rendered as source text")
                    story.append(Paragraph("[Diagram source fallback]", style["small"]))
                    add_code(story, code, style["code"], 86)
            else:
                add_code(story, code, style["code"], 86)
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            depth = len(heading.group(1))
            content = inline_markup(heading.group(2), mono_font)
            if first_heading and depth == 1:
                story.append(Paragraph(content, style["title"]))
                first_heading = False
            else:
                story.append(Paragraph(content, style["h1" if depth == 2 else "h2" if depth == 3 else "h3"]))
            index += 1
            continue
        parsed_table = table_rows(lines, index)
        if parsed_table:
            rows, next_index = parsed_table
            max_columns = max(len(row) for row in rows)
            normalized = [row + [""] * (max_columns - len(row)) for row in rows]
            data = [[Paragraph(inline_markup(cell, mono_font), style["table"]) for cell in row] for row in normalized]
            table = Table(data, colWidths=[None] * max_columns, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), PALE_BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), INK),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.extend([table, Spacer(1, 2.5 * mm)])
            index = next_index
            continue
        if line.lstrip().startswith(">"):
            quote_lines = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                quote_lines.append(lines[index].lstrip()[1:].strip())
                index += 1
            quote = Table(
                [[Paragraph(inline_markup(" ".join(quote_lines), mono_font), style["quote"])]],
                colWidths=[165 * mm],
            )
            quote.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
                ("BOX", (0, 0), (0, -1), 0, colors.white),
                ("LINEBEFORE", (0, 0), (0, -1), 2.2, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([quote, Spacer(1, 2.5 * mm)])
            continue
        list_match = re.match(r"^\s*(?:[-*+] |\d+[.)] )(.+)", line)
        if list_match:
            numbered = bool(re.match(r"^\s*\d+[.)] ", line))
            items = []
            while index < len(lines):
                match = re.match(r"^\s*(?:[-*+] |\d+[.)] )(.+)", lines[index])
                if not match:
                    break
                items.append(ListItem(Paragraph(inline_markup(match.group(1), mono_font), style["body"]), leftIndent=4 * mm))
                index += 1
            story.append(ListFlowable(items, bulletType="1" if numbered else "bullet", leftIndent=6 * mm, bulletFontName=body_font, bulletFontSize=7))
            story.append(Spacer(1, 1.5 * mm))
            continue
        paragraph_lines = [line.strip()]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip() or candidate.startswith("#") or candidate.startswith("```") or candidate.lstrip().startswith(">"):
                break
            if re.match(r"^\s*(?:[-*+] |\d+[.)] )", candidate):
                break
            if table_rows(lines, index):
                break
            paragraph_lines.append(candidate.strip())
            index += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph_lines), mono_font), style["body"]))
    return story, warnings


def solution_files(solution_dir: Path) -> list[Path]:
    result = []
    for path in solution_dir.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in CODE_SUFFIXES or path.name in BUILD_FILENAMES:
            result.append(path)
    return sorted(result, key=lambda item: item.relative_to(solution_dir).as_posix())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def appendix_story(files: Iterable[Path], solution_dir: Path, style: dict[str, ParagraphStyle], mono_font: str) -> list[Flowable]:
    files = list(files)
    story: list[Flowable] = [
        PageBreak(),
        Paragraph("Appendix: Complete Runnable Code", style["h1"]),
        Paragraph(
            "Every production source, test, and required build file from the verified solution is reproduced below. Paths are relative to the article directory.",
            style["body"],
        ),
        Paragraph("Appendix manifest", style["h2"]),
        Preformatted("APPENDIX_MANIFEST_BEGIN", style["appendix_code"]),
    ]
    manifest_lines = []
    for path in files:
        relative = Path("solution") / path.relative_to(solution_dir)
        manifest_lines.append(f"path: {relative.as_posix()}")
        manifest_lines.append(f"sha256: {digest(path)}")
    manifest_lines.append("APPENDIX_MANIFEST_END")
    add_code(story, "\n".join(manifest_lines), style["appendix_code"], 100)
    for path in files:
        relative = Path("solution") / path.relative_to(solution_dir)
        story.append(Paragraph(inline_markup(relative.as_posix(), mono_font), style["appendix_path"]))
        code = path.read_text(encoding="utf-8", errors="replace")
        lines = code.splitlines() or [""]
        page_count = max(1, math.ceil(len(lines) / 90))
        chunk_size = math.ceil(len(lines) / page_count)
        for offset in range(0, len(lines), chunk_size):
            if offset:
                story.append(PageBreak())
                story.append(Paragraph(
                    inline_markup(f"{relative.as_posix()} (continued)", mono_font),
                    style["appendix_path"],
                ))
            add_code(story, "\n".join(lines[offset:offset + chunk_size]), style["appendix_code"], 105)
    return story


def article_title(markdown: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, re.MULTILINE)
    return re.sub(r"[*_`]", "", match.group(1)).strip() if match else fallback


def draw_page(canvas, doc) -> None:  # type: ignore[no-untyped-def]
    canvas.saveState()
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    if doc.page > 1:
        canvas.drawString(20 * mm, A4[1] - 12 * mm, doc.title[:85])
        canvas.setStrokeColor(LINE)
        canvas.line(20 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def main() -> int:
    args = parse_args()
    article = args.article.resolve()
    solution_dir = args.solution_dir.resolve()
    output = (args.output or article.with_suffix(".pdf")).resolve()

    if not article.is_file():
        raise SystemExit(f"Markdown article does not exist: {article}")
    if article.name.lower() == "article.md":
        raise SystemExit("Use a question[-level].md filename, not article.md")
    if not solution_dir.is_dir():
        raise SystemExit(f"Solution directory does not exist: {solution_dir}")
    if output.stem != article.stem:
        raise SystemExit("PDF and Markdown stems must match")

    files = solution_files(solution_dir)
    if not files:
        raise SystemExit("No source, test, or build files found for the PDF appendix")

    markdown = article.read_text(encoding="utf-8")
    title = article_title(markdown, article.stem.replace("-", " ").title())
    body_font, mono_font = register_fonts()
    style = styles(body_font, mono_font)
    story, warnings = markdown_story(markdown, style, body_font, mono_font)
    story.extend(appendix_story(files, solution_dir, style, mono_font))

    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=19 * mm, bottomMargin=16 * mm, title=title, author=args.author,
        subject="Low-level design interview article with complete runnable code",
        allowSplitting=True,
    )
    document.build(story, onFirstPage=draw_page, onLaterPages=draw_page)

    print(f"Created PDF: {output}")
    print(f"Included {len(files)} appendix file(s)")
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    return 0 if not warnings else 2


if __name__ == "__main__":
    raise SystemExit(main())
