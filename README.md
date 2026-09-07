# Useful AI Skills and Agents

A collection of reusable, practical AI skills and agent workflows. The emphasis is on artifacts that are opinionated enough to be useful, transparent about their tradeoffs, and testable where possible.

## Included skills

### `craft-lld-interview-article`

Turns an underspecified low-level design or object-oriented design prompt into an original, interview-sized teaching article with:

- requirements discovery and explicit scope;
- contextual alternatives, including Bad/Good/Great only when the decision earns them;
- requirement-led state and method derivation for every central class;
- UML-lite Mermaid diagrams;
- a focused class and API design;
- a sensibly packaged runnable implementation and tests;
- question-and-level-named Markdown and matching PDF outputs;
- the complete verified codebase in the PDF appendix;
- verification, extensions, and level-specific expectations.

The skill is designed around a typical one-hour interview. It favors the smallest design that preserves the important invariants, shows how each class was earned, and clearly separates interview implementation from production follow-ups.

### `tailor-tech-job-application`

Builds a tailored application package for one or more tech roles with:

- a cited company context dossier saved before drafting when the employer is named;
- a prioritized job analysis and candidate evidence ledger;
- a concise recruiter email and LinkedIn connection note for named employers;
- a contribution-first cover letter;
- 5-6 research-grounded questions for the interviewer when company research is available;
- a truthful one-page tailored resume that preserves the supplied LaTeX format and structure;
- validation for length, sources, LaTeX structure, PDF page count, and common AI-writing tells.

The skill uses current first-party and trustworthy independent sources, excludes anonymous employee reviews and social-media rumors, and prevents unsupported keywords or accomplishments from entering the application.

Each job description is processed in a separate workspace. If a listing does not disclose the employer, the skill continues with a role-focused cover letter and resume instead of inventing company context.

## Install locally

Copy the skill directory into your Codex skills folder:

```bash
cp -R skills/craft-lld-interview-article "$CODEX_HOME/skills/"
cp -R skills/tailor-tech-job-application "$CODEX_HOME/skills/"
```

Restart or reload Codex if needed, then invoke it by name:

```text
Use $craft-lld-interview-article to turn "Design a parking lot" into an article with a runnable Java solution.
Use $tailor-tech-job-application to research this company and tailor my application to the attached tech job description and LaTeX resume project.
Use $tailor-tech-job-application to process these three job descriptions separately against the same LaTeX resume project.
```

## Repository layout

```text
skills/
├── craft-lld-interview-article/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/article-template.md
│   ├── references/
│   └── scripts/
└── tailor-tech-job-application/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    └── scripts/
```

## Principles

- Use original prose and examples.
- Demonstrate design failures with concrete scenarios.
- Treat sophistication as a cost, not an automatic improvement.
- Keep generated code executable and mechanically verified.
- Add diagrams only when they materially improve understanding.
- Preserve candidate truth while adapting application language to the role.
- Ground company-specific application claims in current, cited research.
