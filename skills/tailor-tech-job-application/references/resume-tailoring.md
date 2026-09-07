# Truth-preserving LaTeX resume tailoring

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

## LaTeX source contract

The user supplies the current LaTeX resume project. Treat every source file and local dependency as one project, including `.tex`, `.cls`, `.sty`, bibliography files, fonts, images, and build instructions.

1. Copy the supplied project to `resume-source/original/` without editing it.
2. Copy the same project to `resume-source/tailored/` and make content edits there.
3. Preserve relative paths and filenames between the two copies.
4. Identify the main `.tex` file and original compiler from the project, such as a TeX magic comment, README, Makefile, or existing build command.
5. Compile the original copy first. Its successful PDF is the visual baseline.

If only a PDF is available, do not reconstruct it in another format or template. Ask the user for the LaTeX project before tailoring the resume.

## Content-only default

The resume is layout-locked for every new application. Unless the current user explicitly asks for a redesign of this resume in the current task, preserve all formatting and structural choices, including:

- document class, packages, preamble, custom commands, and build engine;
- page size, margins, columns, typography, colors, rules, icons, and spacing;
- section names and order;
- role, project, education, and skill-entry order;
- the number and order of bullets and entries;
- headers, footers, links, alignment, and visual hierarchy.

Do not replace the LaTeX template, convert it to another authoring system, run a broad formatter, or make the layout more ATS-oriented on your own. If the current format creates an ATS or readability concern, report it separately and leave the structure unchanged.

A request to tailor, improve, optimize, make the resume fit, or strengthen ATS alignment is not permission to alter layout. Approval from another role, resume, conversation, or user is not transferable.

Content edits may adjust summary wording, skill emphasis, and the wording inside an existing bullet or entry. Keep every change within the candidate evidence ledger. A content edit should not add a new structural command, section, environment, bullet, or entry.

## Select changes by evidence

Classify each proposed content change:

- **Clarify:** replace niche wording with an equivalent term used by the job description.
- **Emphasize:** make an existing action, technical judgment, or outcome easier to scan.
- **Compress:** shorten supported content to protect the one-page limit.
- **Substitute:** replace lower-priority wording with a more relevant supported fact while retaining the same structural slot.
- **Reject:** decline a keyword or claim that the source resume does not support.

Use job keywords only in context. Repeated and early job-description terms deserve more attention, but evidence decides whether they appear.

## Bullet editing

A strong tech resume bullet usually makes these elements clear when the source supports them:

`action + system or problem + technical method or judgment + outcome`

Do not force all four into every bullet. Preserve concise original bullets that already communicate the right evidence.

Avoid first person, vague claims, keyword lists disguised as prose, and marketing language. Use ordinary hyphens instead of em dashes.

## One-page fit without redesign

The compiled tailored PDF must be exactly one page. After each meaningful edit, compile and inspect the page count and visual result.

If content overflows or creates poor wrapping, fix it in this order:

1. Shorten the new wording while preserving meaning.
2. Remove redundant phrases introduced during tailoring.
3. Prefer a shorter supported keyword or phrase.
4. Undo a lower-priority tailoring change.
5. Restore the original wording for the affected slot.

Do not solve overflow by changing margins, font size, line spacing, column widths, section spacing, page geometry, or template macros unless the user explicitly authorizes a format or structure change.

## Required change log

For every material content edit, record:

| Location | Original | Tailored | Change type | Evidence | Reason |
| --- | --- | --- | --- | --- | --- |

Also list:

- job keywords used;
- important keywords omitted because they were unsupported;
- content compressed or restored to maintain one page;
- the main `.tex` file, compiler, and build command;
- whether source structure and formatting commands remained unchanged;
- any user-authorized format or structure change.

## Compile, compare, and verify

Before delivery:

1. Compile both `resume-source/original/` and `resume-source/tailored/` with the same engine and build process.
2. Confirm the original and tailored PDFs each have exactly one page.
3. Render both PDFs to images at the same resolution.
4. Compare them visually. Verify that typography, margins, columns, section positions, spacing system, and hierarchy retain the original design.
5. Inspect the tailored page at normal reading size for clipping, overlap, orphaned headings, awkward wraps, inconsistent alignment, and unbalanced whitespace.
6. Extract text from the tailored PDF and confirm the content is selectable and complete.
7. Compare every date, title, employer, metric, and technology against the source resume and candidate evidence ledger.
8. Review the LaTeX diff. It should contain content changes only unless the user requested otherwise.
9. Run `scripts/validate_application.py` on the full application directory.

For ordinary tailoring, run the validator without `--allow-format-change`. Any locked-mode layout error must be fixed by restoring the original layout and revising content. Do not use the override to silence a failed check.

When the user has explicitly requested a format or structure change, record the exact request in an application-local `format-change-approval.md`:

```markdown
# User-authorized resume format change

User request: <exact user instruction>

## Approved changes

- <specific authorized change>
```

Only then may validation use both `--allow-format-change` and `--format-change-approval path/to/format-change-approval.md`. The approval record does not authorize changes beyond its listed scope.

Revise content until the PDF fits and looks polished. Do not deliver an uncompiled `.tex` file, claim that it fits based only on source length, or claim format preservation without a successful locked validation and visual comparison.
