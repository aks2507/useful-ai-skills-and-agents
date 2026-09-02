# Truth-preserving resume tailoring and PDF workflow

Read this file before editing a resume.

## Preserve the record

The existing resume is the source of truth. Preserve:

- employers, clients, schools, roles, dates, locations, and reporting scope;
- technologies actually used;
- metrics and units exactly as supported;
- project goals, ownership, and outcomes;
- education, certifications, publications, awards, and links.

Do not add a skill merely because it appears in the job description. Do not turn exposure into ownership, participation into leadership, prototypes into production systems, team outcomes into individual outcomes, or approximate scale into a precise metric.

When a term is ambiguous, retain the original meaning or ask the user. If the resume says `cloud platform`, a job posting that says `AWS` does not establish AWS experience.

## Inspect before editing

1. Preserve the original PDF unchanged.
2. Extract its text and inspect the visual rendering.
3. Identify the current reading order, sections, typography, margins, columns, and any parsing problems.
4. Build `candidate-evidence.md` before rewriting.
5. Prefer the original editable source when available. Otherwise reconstruct a clean editable source and record that in `resume-change-log.md`.

Use the environment's document and PDF tooling. If installed skills provide document or PDF-specific render-and-verify instructions, load and follow them.

## Select changes by evidence

Classify each proposed change:

- **Reorder:** move the most relevant supported material earlier.
- **Trim:** remove lower-value detail to protect one-page readability.
- **Clarify:** replace niche wording with an equivalent term used by the job description.
- **Emphasize:** make the action, technical judgment, or outcome easier to scan.
- **Reject:** decline a keyword or claim that the source resume does not support.

Use job keywords only in context. Repeated and early job-description terms deserve more attention, but evidence decides whether they appear.

Keep the chronological order of dated experience. Reordering bullets within a role is usually safer than reordering roles.

## Bullet editing

A strong tech resume bullet usually makes these elements clear when the source supports them:

`action + system or problem + technical method or judgment + outcome`

Do not force all four into every bullet. Preserve concise original bullets that already communicate the right evidence.

Avoid first person, vague claims, keyword lists disguised as prose, and marketing language. Use ordinary hyphens instead of em dashes.

## One-page and ATS constraints

The tailored PDF must be exactly one page.

Prefer:

- a single main reading order;
- standard section names such as `Experience`, `Skills`, `Projects`, and `Education`;
- selectable text;
- common fonts at a readable size;
- standard bullets;
- consistent dates and alignment;
- visible email, phone, location, portfolio, GitHub, or LinkedIn only when present in the source.

Avoid:

- text embedded as an image;
- tables, text boxes, charts, icons carrying meaning, headers or footers with essential content, and multi-column layouts that scramble extraction;
- tiny fonts, crowded margins, or aggressive line compression merely to fit one page;
- skill bars or ATS scoring claims.

If the source resume has a complex design, preserve its visual identity only where that does not damage readability or extraction.

## Fit strategy when space is tight

Use this order:

1. Remove repeated wording and generic summaries.
2. Trim weak or old bullets that do not support the target role.
3. Compress skills into evidence-backed categories.
4. Tighten spacing conservatively.
5. Reduce font size only within a professional, readable range.

Do not delete a major career entry, change dates, or hide a material fact solely to improve perceived fit.

## Required change log

For every material edit, record:

| Location | Original | Tailored | Change type | Evidence | Reason |
| --- | --- | --- | --- | --- | --- |

Also list:

- job keywords used;
- important keywords omitted because they were unsupported;
- content removed for space;
- any formatting reconstructed from the PDF.

## Render and verify

Before delivery:

1. Export `tailored-resume.pdf` from the editable source.
2. Confirm it has exactly one page.
3. Render the page to an image and inspect it at normal reading size.
4. Check clipping, overlap, orphaned headings, uneven spacing, weak hierarchy, and small text.
5. Extract text from the final PDF and confirm the reading order is sensible.
6. Compare every date, title, employer, metric, and technology against the source resume.
7. Run `scripts/validate_application.py` on the full application directory.

Revise until both the visual and extracted-text checks pass.

## Basis for ATS guidance

The layout and keyword principles align with current MIT career guidance: use straightforward formatting, integrate relevant terms meaningfully, retain common file formats, and avoid keyword stuffing or falsification.

- [MIT CAPD: Make your resume ATS-friendly](https://capd.mit.edu/resources/make-your-resume-ats-friendly/)
- [MIT CAPD: Career toolkit, crafting an effective resume](https://capd.mit.edu/resources/career-toolkit-crafting-an-effective-resume/)
