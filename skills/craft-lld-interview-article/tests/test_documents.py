"""Rendering regressions; run with unittest discover -s tests from the skill."""

import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_pdf as pdf
import validate_article as validator
from pypdf import PdfReader
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate


SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="300">
<rect width="800" height="300" fill="#eef3ff"/>
<text x="20" y="80" font-family="Helvetica" font-size="24">Vote replaced</text>
</svg>'''


class DocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body, cls.mono = pdf.register_fonts()
        cls.styles = pdf.styles(cls.body, cls.mono)

    def test_body_emphasis_uses_distinct_font_faces(self):
        paragraph = Paragraph(pdf.inline_markup("plain **bold** *italic*", self.mono), self.styles["body"])
        faces = {fragment.text.strip(): fragment.fontName for fragment in paragraph.frags if fragment.text.strip()}
        self.assertNotEqual(faces["plain"], faces["bold"])
        self.assertNotEqual(faces["plain"], faces["italic"])
        self.assertEqual(self.styles["h1"].fontName, faces["bold"])

    def test_relation_types_and_multiplicities_survive_parsing(self):
        _, edges = pdf.ClassDiagram._parse('''classDiagram
  Question "1" *-- "0..*" Answer : owns
  Answer --|> Post : extends
  Forum --> Post : indexes
  Sink <|.. ConsoleSink : implements
''')
        self.assertEqual(edges[0], ("Question", "Answer", "owns", "*--", "1", "0..*"))
        self.assertEqual([edge[3] for edge in edges[1:]], ["--|>", "-->", "<|.."])

    def test_svg_aspect_ratio_and_caption_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "figure.svg").write_text(SVG)
            figure = pdf.local_figure("figure.svg", root)
            self.assertAlmostEqual(figure.width / figure.height, 8 / 3)
            story, warnings = pdf.markdown_story(
                "## A decision\n\n![A replaced vote](figure.svg)\n\n*Figure 1. One choice remains.*",
                self.styles, self.body, self.mono, root,
            )
            self.assertFalse(warnings)
            self.assertIsInstance(story[0], KeepTogether)
            self.assertEqual(len(story[0]._content), 4)  # heading, figure, spacer, caption
            output = io.BytesIO()
            SimpleDocTemplate(output).build(story)
            text = PdfReader(output).pages[0].extract_text()
            self.assertIn("Vote replaced", text)
            self.assertIn("Figure 1. One choice remains.", text)

    def test_missing_and_remote_figures_fail_loudly(self):
        with tempfile.TemporaryDirectory() as directory:
            for source in ("missing.svg", "https://example.com/a.png", "../escape.svg", "/tmp/a.png"):
                with self.subTest(source=source), self.assertRaises(ValueError):
                    pdf.local_figure(source, Path(directory))

    def test_svg_external_resources_are_not_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            samples = [
                '<svg><image href="https://example.com/a.png"/></svg>',
                '<svg><use href="file:///tmp/a.svg"/></svg>',
                '<!DOCTYPE svg SYSTEM "https://example.com/a.dtd"><svg/>',
                '<svg><style>@import "https://example.com/a.css";</style></svg>',
                '<svg><rect fill="url(https://example.com/a.svg)"/></svg>',
                '<svg><script>bad()</script></svg>',
            ]
            for source in samples:
                (root / "bad.svg").write_text(source)
                with self.subTest(source=source), self.assertRaises(ValueError):
                    pdf.local_figure("bad.svg", root)

    def test_mermaid_heading_stays_with_diagram(self):
        story, warnings = pdf.markdown_story("## Model\n\n```mermaid\nclassDiagram\n class Post\n```", self.styles, self.body, self.mono)
        self.assertFalse(warnings)
        self.assertIsInstance(story[0], KeepTogether)
        self.assertIsInstance(story[0]._content[0], Paragraph)

    def test_prose_introduction_stays_with_its_code(self):
        story, _ = pdf.markdown_story("## Vote\n\nApply this change:\n\n```text\nvotes[user] = choice\n```", self.styles, self.body, self.mono)
        self.assertIsInstance(story[0], KeepTogether)
        self.assertEqual(story[0]._content[0].getPlainText(), "Vote")
        self.assertEqual(story[0]._content[1].getPlainText(), "Apply this change:")

    def test_pdf_has_real_bold_and_italic(self):
        output = io.BytesIO()
        paragraph = Paragraph(pdf.inline_markup("Normal **important** *caption*", self.mono), self.styles["body"])
        SimpleDocTemplate(output).build([paragraph])
        fonts = PdfReader(output).pages[0]["/Resources"]["/Font"].get_object()
        names = [str(font.get_object()["/BaseFont"]) for font in fonts.values()]
        self.assertTrue(any("Bold" in name for name in names), names)
        self.assertTrue(any("Italic" in name or "Oblique" in name for name in names), names)

    def test_validator_warns_about_prose_only_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            article = Path(directory) / "sample.md"
            article.write_text("# Design Sample\n\n## Extensibility\n\n### Cache\n\nAdd a cache.")
            _, warnings = validator.validate_article(article, None)
            self.assertTrue(any("no code delta" in warning for warning in warnings))

    def test_adjacent_nonempty_code_blocks_are_not_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            article = Path(directory) / "sample.md"
            article.write_text("# Design Sample\n\n```text\none\n```\n\n```text\ntwo\n```")
            errors, _ = validator.validate_article(article, None)
            self.assertFalse(any("empty fenced" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
