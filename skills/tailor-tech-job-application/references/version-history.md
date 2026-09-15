# Skill version history

Read this file only when the freshness check reports that an existing application was created with an older skill version.

## 1.1.0

- Replaced achievement-driven cover-letter drafting with a narrative about specific interest, credible fit, contribution, and career direction.
- Added a private narrative plan and editorial acceptance review in the candidate evidence ledger. A brief example supports the story; past achievements should occupy a minority of the letter.
- Made quantified results optional and added advisory checks for dense numerical detail and list formatting. Zero warnings do not establish narrative quality.
- Distinguished candidate-stated motivation from a proposed editorial angle. Prior generated prose is not a source of candidate facts.
- Applied the same narrative standard to anonymous-company letters and added primary MIT and Harvard career-guidance sources.
- Preserved the resume layout lock, one-page rendering requirements, outreach limits, and independent processing of multiple jobs.

When resuming a 1.0.0 application, reread `references/application-writing.md` and review the cover letter even if it previously passed automated validation. Recheck facts copied from prior generated drafts, record the narrative plan and editorial findings, and rewrite letters dominated by achievements, numbers, or technology lists. Audit the requested artifacts against current instructions before recording reconciled state; do not bless stale prose by changing only its version record.

## 1.0.0

- Added a per-invocation freshness gate and a content-addressed skill manifest.
- Added per-application `skill-state.json` records so resumed work detects instruction changes.
- Made current on-disk skill instructions authoritative over older copies or summaries in chat context.
- Added fail-closed LaTeX layout validation. A format-change override now requires a current, application-local record of explicit user authorization.
- Added exact preamble, section-order, body-layout, and ancillary-project-file comparisons.
- Preserved named-company, anonymous-company, multi-job, research, writing, interviewer-question, and one-page resume behavior.

For an application created before 1.0.0, reread the current `SKILL.md` and all references needed for the requested work. Audit the existing application against the current output contract, run the current validator, and record the current state only after all new requirements pass.
