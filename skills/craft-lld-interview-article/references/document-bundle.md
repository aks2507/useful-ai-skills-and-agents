# Markdown, PDF, and Source Bundle

## Naming

Keep this skill's generated bundles under `skills/craft-lld-interview-article/generated-content/<problem-slug>/` in the repository. This is the default scaffold destination. Honor an explicitly requested alternative path, and keep source links relative to the article. Do not create a shared repository-root output directory for unrelated skills.

Slugify the question title in lowercase kebab case.

- Explicit junior request: `vending-machine-junior.md` and `vending-machine-junior.pdf`.
- Explicit senior request: `inventory-management-senior.md` and `inventory-management-senior.pdf`.
- No explicit level: `parking-lot.md` and `parking-lot.pdf`.

Never ship final files named `article.md` or `article.pdf`. Markdown and PDF stems must match.

## One article, two formats

The finalized Markdown is the source of truth for the PDF body. Do not separately rewrite or summarize the PDF. This prevents changes in requirements, class names, diagrams, commands, and verification results from drifting between formats.

Build the PDF only after code and prose verification. Rebuild it after every substantive Markdown or source change.

## Self-contained PDF

The PDF must contain:

1. the full Markdown article in the same section order;
2. readable diagrams derived from the article's diagram source;
3. exact compile, test, and demo commands with observed results;
4. **Appendix: Complete Runnable Code**;
5. every production source file;
6. every test file;
7. required build or package metadata;
8. relative paths and a SHA-256 manifest so the appendix can be checked against disk.

Routine code may remain out of the Markdown narrative, but it may not be omitted from the PDF appendix.

The appendix reproduces the same interview-sized application. It is not a place for extra hardening, alternate implementations, or speculative helpers. Label additional tests as study support in the article.

## Build command

Use:

```bash
python3 scripts/build_pdf.py path/to/question[-level].md \
  --solution-dir path/to/solution
```

The output defaults to the Markdown path with a `.pdf` suffix. The builder uses ReportLab. Prefer the Codex bundled PDF Python runtime when the system Python does not provide it.

The built-in renderer draws a compact vector form of supported Mermaid class, state, and sequence diagrams. Unsupported diagram syntax remains visible as a labeled source block; treat that fallback as a release failure when the diagram is required to understand the design.

## Visual verification

Render every PDF page to PNG and inspect the montage plus any dense pages at full size. Check:

- no clipped text or diagrams;
- readable font size;
- no table cell overflow;
- code lines wrap or continue legibly;
- headings stay with following content when practical;
- no accidental blank pages;
- appendix paths, code, and manifest are complete.

Text extraction is useful for completeness checks but does not replace visual inspection.

## Parity verification

Run `validate_article.py` with both `--solution-dir` and `--pdf`. It checks the shared stem, PDF title/section presence, appendix paths, and file checksums. It cannot prove good visual layout; the rendered-page inspection remains mandatory.
