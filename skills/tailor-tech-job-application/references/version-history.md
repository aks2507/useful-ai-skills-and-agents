# Skill version history

Read this file only when the freshness check reports that an existing application was created with an older skill version.

## 1.0.0

- Added a per-invocation freshness gate and a content-addressed skill manifest.
- Added per-application `skill-state.json` records so resumed work detects instruction changes.
- Made current on-disk skill instructions authoritative over older copies or summaries in chat context.
- Added fail-closed LaTeX layout validation. A format-change override now requires a current, application-local record of explicit user authorization.
- Added exact preamble, section-order, body-layout, and ancillary-project-file comparisons.
- Preserved named-company, anonymous-company, multi-job, research, writing, interviewer-question, and one-page resume behavior.

For an application created before 1.0.0, reread the current `SKILL.md` and all references needed for the requested work. Audit the existing application against the current output contract, run the current validator, and record the current state only after all new requirements pass.
