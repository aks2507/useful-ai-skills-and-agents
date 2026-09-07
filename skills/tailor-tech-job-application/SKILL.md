---
name: tailor-tech-job-application
description: Create, continue, revise, or validate truthful application materials and a one-page LaTeX resume for one or more tech job descriptions while preserving the supplied resume format. When a company is named, research it and create outreach, a cover letter, and interviewer questions; when it is undisclosed, create a role-focused cover letter and tailored resume. Do not use for non-tech roles, bulk outreach, or inventing qualifications.
---

# Tailor Tech Job Application

Build one coherent application narrative from current company research when available, the job description, and the candidate's verified experience. Produce the full application package or the subset the user requests.

## Mandatory freshness gate

At the beginning of every invocation and every follow-up that continues application work, before relying on prior chat context or existing artifacts, locate this skill's directory from the loaded `SKILL.md` path and run:

```bash
python3 scripts/check_skill_freshness.py
```

State the reported version and short digest in a concise progress update. The current on-disk `SKILL.md`, references, and scripts supersede every older copy, paraphrase, plan, or summary of this skill in the chat. Current user instructions retain their normal priority.

If the checker reports a partial manifest or a duplicate skill copy, do not continue the application workflow. Resolve the installation so there is one canonical current copy. Never choose between same-name copies by guesswork.

When resuming an existing application directory, also run:

```bash
python3 scripts/check_skill_freshness.py --state-file path/to/application/skill-state.json
```

If the application state is missing or stale, read `references/version-history.md`, reread every current reference required for the requested work, and audit the existing artifacts against the current instructions. Rebuild or revise anything that no longer complies and run the current application validator. When the missing or stale state is the only remaining validation error, record the current state with `--record-state`, then rerun validation. Do not record a new state merely to silence other failures.

For a new application, `scripts/scaffold_application.py` records `skill-state.json` automatically. A running turn cannot be retroactively changed, so if the skill changes during an active turn, finish no deliverable from the old instructions. Rerun the freshness gate and restart that workflow step using the new version.

## Scope gate

Use this skill only for tech roles, including software engineering, data, machine learning, infrastructure, cloud, security, technical product, developer relations, solutions engineering, and closely related leadership roles.

If the role is clearly non-technical, explain that this skill is optimized for tech applications and stop. If the role is mixed, proceed only when technical judgment or delivery is central to the job.

## Required inputs

Obtain:

1. One or more complete job descriptions or accessible job URLs.
2. The company name associated with each description, when it is disclosed.
3. The candidate's current LaTeX resume project, including the main `.tex` file, local classes, styles, fonts, images, bibliography files, and build instructions it depends on.
4. The current compiled resume PDF when available, for visual comparison.

Use the role title and recruiter name when available. Never invent a recruiter, team, location, reporting line, technology, metric, employment fact, or personal motivation.

The LaTeX source is required for resume tailoring because the existing format and structure must be preserved. If the user supplies only a PDF, complete non-resume deliverables when requested, but ask for the LaTeX project before editing the resume. Do not reconstruct the resume in a different template.

Ask a question only when a required artifact is unavailable or ambiguity could make the application factually wrong. A missing recruiter name is not blocking; use a neutral greeting.

## Application modes and batches

Process every job description independently. Create a separate workspace, research context, job analysis, evidence mapping, prose set, LaTeX copy, PDF, and validation result for each role. Never combine company facts, role keywords, contribution theses, or resume edits across descriptions.

When several descriptions share one candidate resume, start every tailored copy from the unchanged supplied LaTeX project. If the user provides different resumes for different roles, preserve that mapping.

Use one mode for each description:

- **Named-company mode:** Research the named employer and produce the full application package.
- **Anonymous-company mode:** If the listing does not identify the employer, continue without company research. Produce only the contribution-led cover letter and tailored resume as user-facing artifacts. Build `job-analysis.md` and `candidate-evidence.md` as working evidence, and do not invent a company, mission, product, recruiter, or culture.

Do not let an anonymous listing block other descriptions in the same request.

## Load the guidance

Before working:

- Complete the mandatory freshness gate. Read `references/version-history.md` only for a missing or stale application state.
- In named-company mode, read `references/company-research.md` for source selection and the required company context dossier.
- Read `references/application-writing.md` before drafting public-facing prose.
- In named-company mode, read `references/interviewer-questions.md` before drafting questions for the interviewer.
- Read `references/resume-tailoring.md` before changing the resume or generating its PDF.

When filesystem artifacts are requested, run `scripts/scaffold_application.py` to create the workspace without overwriting existing work.

## Workflow

### 1. Research and save company context when the company is named

For named-company mode, browse the current web. Start with first-party sources, then corroborate with reliable independent or regulatory sources. Exclude social-media rumors, anonymous commentary, Glassdoor, and employee-review sites.

Research until additional trustworthy sources stop changing the role-relevant picture. Save the findings to `company-context.md` before drafting any application material. Separate sourced facts from reasoned inferences and cite every material claim with a direct link.

Do not call the research exhaustive. Record important unknowns and conflicting evidence.

For anonymous-company mode, skip company research and `company-context.md`. Analyze only the supplied job description and record the missing company identity under `job-analysis.md` unknowns.

### 2. Analyze the job description

Save `job-analysis.md` with:

- the role's mission and likely outcomes;
- responsibilities and qualifications ranked by repetition, order, and specificity;
- technical, domain, collaboration, and leadership keywords;
- explicit requirements versus preferences;
- signals about the team's immediate problems;
- details that are unclear or absent.

Treat the job description as evidence of hiring priorities, not proof of broader company strategy.

### 3. Build the candidate evidence ledger

Extract the resume into a working text representation. Save `candidate-evidence.md` with three classes:

- **Supported:** directly stated facts, skills, scope, and metrics.
- **Safe rephrasing:** semantically equivalent language that better matches the job description.
- **Unsupported:** requirements or keywords that the resume does not establish.

Map the strongest supported evidence to the role's highest priorities. Keep unsupported items out of every deliverable. Ask the user for missing evidence only when it could materially improve the application.

### 4. Establish one contribution thesis

Write a private one or two sentence thesis that connects:

`company or role problem -> role outcome -> candidate evidence -> distinctive contribution`

Use this thesis as the common spine for all deliverables. Vary the wording and depth by format so the package feels consistent without repeating itself.

### 5. Draft the outreach, cover letter, and interview questions

In named-company mode, create:

- `recruiter-email.md`, no more than 200 words including the subject line;
- `linkedin-connection.md`, within the current platform limit, or 200 characters when the limit is unknown;
- `cover-letter.md`, concise enough for one page and shaped around contribution first, with career growth as a smaller supporting theme.
- `interviewer-questions.md`, containing 5-6 concise questions the candidate can ask at the end of an interview.

Follow `references/application-writing.md` and `references/interviewer-questions.md`. Prefer specific, plain language over inflated claims. Demonstrate strong suitability through evidence rather than declaring the candidate the best. Ground at least four interview questions in the company's work, current challenges, or problem-solving approach, using `company-context.md` rather than generic interview lists.

In anonymous-company mode, create only `cover-letter.md` and the tailored resume as user-facing artifacts. The cover letter should focus on what the candidate can bring to the role using the job analysis and evidence ledger. Use a neutral greeting and omit company-specific motivation, claims, recruiter outreach, LinkedIn outreach, and interviewer questions.

### 6. Tailor the resume

The supplied resume is layout-locked by default. Copy the LaTeX project into `resume-source/original/` unchanged and make the tailored copy in `resume-source/tailored/` with the same relative file structure. Preserve the template, preamble, macros, section order, columns, typography, colors, spacing, and number and order of entries and bullets. Change only wording inside existing content slots.

Do not infer permission to change format or structure from a request to tailor, improve, optimize, fit one page, improve ATS compatibility, or fix an overflow. Permission exists only when the user explicitly requests a format or structure change for this resume in the current task. Earlier approval for another resume, role, task, or user does not carry over.

Preserve the candidate's employment history, dates, titles, education, metrics, project facts, and core achievements. Tailor summary text, skill emphasis, and bullet wording only when supported by the evidence ledger. If the edited text overflows, shorten or undo lower-priority wording before considering any layout change.

Compile the tailored LaTeX project with its existing engine and build process to create `tailored-resume.pdf`. Confirm it is exactly one page, render it to an image, compare it with the original, and inspect it for clipping, overlap, awkward wrapping, spacing regressions, and visual imbalance. Save `resume-change-log.md` with each material content edit and explicit confirmation that format and structure were preserved.

Before delivery, the application validator must pass in its default locked mode. Do not use `--allow-format-change` to get around a failure. Restore the layout-changing edit and shorten or undo content changes instead. Do not claim that the resume is complete or layout-preserved when the locked validation or visual comparison has not passed.

If the current user explicitly requests a format or structure change, create `format-change-approval.md` inside that role's application directory. Quote the user's exact instruction on a `User request:` line and list only the authorized changes under `## Approved changes`. Then, and only then, the validator may be run with both `--allow-format-change` and `--format-change-approval path/to/format-change-approval.md`. Never create this approval record merely because locked validation failed.

Follow `references/resume-tailoring.md` for the truth-preserving and PDF checks.

### 7. Cross-check the package

Verify that:

- in named-company mode, company-specific statements appear in `company-context.md` with citations;
- in anonymous-company mode, public materials contain no invented company context;
- candidate claims appear in `candidate-evidence.md` as supported or safe rephrasing;
- no deliverable implies experience with an unsupported requirement;
- in named-company mode, the email, connection note, cover letter, and resume share a contribution thesis without duplicating paragraphs;
- in anonymous-company mode, the cover letter and resume share the role-focused contribution thesis without duplicating wording;
- in named-company mode, `interviewer-questions.md` contains 5-6 useful questions, with at least four traceable to company research;
- names, titles, dates, metrics, technologies, and locations agree across files;
- no public-facing artifact uses an em dash, a `not X but Y` construction, canned AI prose, or unsupported superlatives;
- the original and tailored LaTeX projects retain the same source structure and formatting commands unless the user requested a change;
- the resume PDF is one page and its text can be extracted in a sensible reading order.

Run:

```bash
python3 scripts/validate_application.py path/to/application-directory
```

For an undisclosed employer, run:

```bash
python3 scripts/validate_application.py path/to/application-directory --anonymous-company
```

Fix all errors. A successful exit in the default mode is mandatory for a content-only resume. Review warnings manually rather than rewriting good prose merely to silence a heuristic.

Immediately before delivery, rerun the freshness checker with the application state file. If its version or digest differs from the value reported at the start of the turn, the skill changed during the run. Reconcile against the new version and repeat affected validation before delivering anything.

## Output contract

Use this layout for named-company mode:

```text
<company>-<role>/
|-- skill-state.json
|-- company-context.md
|-- job-analysis.md
|-- candidate-evidence.md
|-- recruiter-email.md
|-- linkedin-connection.md
|-- cover-letter.md
|-- interviewer-questions.md
|-- resume-change-log.md
|-- tailored-resume.pdf
`-- resume-source/
    |-- original/    # unchanged supplied LaTeX project
    `-- tailored/    # content-edited copy with the same structure
```

The company context, job analysis, and evidence ledger are part of the deliverable. They make the public artifacts auditable and reusable in later application steps.

For anonymous-company mode, omit `company-context.md`, `recruiter-email.md`, `linkedin-connection.md`, and `interviewer-questions.md`. Keep `skill-state.json`, `job-analysis.md`, and `candidate-evidence.md` as working evidence alongside the cover letter and resume files.

## Non-negotiable constraints

- Run the freshness gate on every invocation and treat the current on-disk skill version as authoritative over stale chat context.
- Never validate or deliver an application whose `skill-state.json` is missing or stale.
- Research each named company before drafting and save that research.
- If the company is undisclosed, continue in anonymous-company mode without company research or invented context.
- Process multiple job descriptions separately from the same unchanged LaTeX baseline.
- For named companies, use current sources instead of relying on model memory.
- Exclude social-media rumors, anonymous reviews, Glassdoor, and employee-review sites from company context.
- Never fabricate or inflate candidate experience, metrics, skills, titles, or responsibilities.
- Do not stuff keywords or insert company language where the candidate has no matching experience.
- Keep the recruiter email at or below 200 words.
- In named-company mode, provide exactly 5-6 interviewer questions, predominantly grounded in company research.
- Preserve the supplied LaTeX resume format and structure. Change either only when the user explicitly requests it.
- Treat resume layout preservation as a per-task lock. Never reuse or infer format-change approval.
- Keep the tailored resume PDF to exactly one page.
- Compile, render, and visually inspect the tailored resume before delivery. Resolve overflow through content editing first.
- Do not deliver a content-only tailored resume unless the default locked validator passes.
- Avoid em dashes, false contrasts such as `not X but Y`, generic praise, and formulaic AI-sounding phrasing in every public-facing artifact.
- Optimize the package for a human technical reader and ordinary ATS parsing, not a speculative ATS score.
