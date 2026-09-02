---
name: tailor-tech-job-application
description: Research a company and tailor recruiter outreach, a LinkedIn connection note, a cover letter, and a truthful one-page PDF resume for a specific software, data, infrastructure, security, product engineering, or other tech role. Use for individual tech job applications when Codex has a job description and an existing resume. Do not use for non-tech roles, bulk outreach, or inventing candidate qualifications.
---

# Tailor Tech Job Application

Build one coherent application narrative from current company research, the job description, and the candidate's verified experience. Produce the full application package or the subset the user requests.

## Scope gate

Use this skill only for tech roles, including software engineering, data, machine learning, infrastructure, cloud, security, technical product, developer relations, solutions engineering, and closely related leadership roles.

If the role is clearly non-technical, explain that this skill is optimized for tech applications and stop. If the role is mixed, proceed only when technical judgment or delivery is central to the job.

## Required inputs

Obtain:

1. The complete job description or an accessible job URL.
2. The company name.
3. The candidate's current resume, preferably the original PDF plus any editable source.

Use the role title and recruiter name when available. Never invent a recruiter, team, location, reporting line, technology, metric, employment fact, or personal motivation. If an editable resume source is absent, reconstruct a clean source from the PDF and record that choice.

Ask a question only when a required artifact is unavailable or ambiguity could make the application factually wrong. A missing recruiter name is not blocking; use a neutral greeting.

## Load the guidance

Before working:

- Read `references/company-research.md` for source selection and the required company context dossier.
- Read `references/application-writing.md` before drafting public-facing prose.
- Read `references/resume-tailoring.md` before changing the resume or generating its PDF.

When filesystem artifacts are requested, run `scripts/scaffold_application.py` to create the workspace without overwriting existing work.

## Workflow

### 1. Research and save company context

Browse the current web for every application. Start with first-party sources, then corroborate with reliable independent or regulatory sources. Exclude social-media rumors, anonymous commentary, Glassdoor, and employee-review sites.

Research until additional trustworthy sources stop changing the role-relevant picture. Save the findings to `company-context.md` before drafting any application material. Separate sourced facts from reasoned inferences and cite every material claim with a direct link.

Do not call the research exhaustive. Record important unknowns and conflicting evidence.

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

`company problem -> role outcome -> candidate evidence -> distinctive contribution`

Use this thesis as the common spine for all deliverables. Vary the wording and depth by format so the package feels consistent without repeating itself.

### 5. Draft the outreach and cover letter

Create:

- `recruiter-email.md`, no more than 200 words including the subject line;
- `linkedin-connection.md`, within the current platform limit, or 200 characters when the limit is unknown;
- `cover-letter.md`, concise enough for one page and shaped around contribution first, with career growth as a smaller supporting theme.

Follow `references/application-writing.md`. Prefer specific, plain language over inflated claims. Demonstrate strong suitability through evidence rather than declaring the candidate the best.

### 6. Tailor the resume

Preserve the candidate's employment history, dates, titles, education, metrics, project facts, and core achievements. Reorder, trim, and rephrase only when doing so improves relevance or clarity without changing meaning.

Generate an editable source and `tailored-resume.pdf`. Keep the PDF to exactly one page, use an ATS-readable layout, and visually inspect the rendered page. Save `resume-change-log.md` with each material change and its supporting source fact.

Follow `references/resume-tailoring.md` for the truth-preserving and PDF checks.

### 7. Cross-check the package

Verify that:

- company-specific statements appear in `company-context.md` with citations;
- candidate claims appear in `candidate-evidence.md` as supported or safe rephrasing;
- no deliverable implies experience with an unsupported requirement;
- the email, connection note, cover letter, and resume share a contribution thesis without duplicating paragraphs;
- names, titles, dates, metrics, technologies, and locations agree across files;
- no public-facing artifact uses an em dash, a `not X but Y` construction, canned AI prose, or unsupported superlatives;
- the resume PDF is one page and its text can be extracted in a sensible reading order.

Run:

```bash
python3 scripts/validate_application.py path/to/application-directory
```

Fix all errors. Review warnings manually rather than rewriting good prose merely to silence a heuristic.

## Output contract

Use this layout when creating files:

```text
<company>-<role>/
|-- company-context.md
|-- job-analysis.md
|-- candidate-evidence.md
|-- recruiter-email.md
|-- linkedin-connection.md
|-- cover-letter.md
|-- resume-change-log.md
|-- tailored-resume.pdf
`-- resume-source/
    `-- editable source and any render support files
```

The company context, job analysis, and evidence ledger are part of the deliverable. They make the public artifacts auditable and reusable in later application steps.

## Non-negotiable constraints

- Research the company before drafting and save that research.
- Use current sources instead of relying on model memory.
- Exclude social-media rumors, anonymous reviews, Glassdoor, and employee-review sites from company context.
- Never fabricate or inflate candidate experience, metrics, skills, titles, or responsibilities.
- Do not stuff keywords or insert company language where the candidate has no matching experience.
- Keep the recruiter email at or below 200 words.
- Keep the tailored resume PDF to exactly one page.
- Avoid em dashes, false contrasts such as `not X but Y`, generic praise, and formulaic AI-sounding phrasing in every public-facing artifact.
- Optimize the package for a human technical reader and ordinary ATS parsing, not a speculative ATS score.
