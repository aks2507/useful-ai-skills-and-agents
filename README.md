# Useful AI Skills and Agents

A collection of reusable, practical AI skills and agent workflows. The emphasis is on artifacts that are opinionated enough to be useful, transparent about their tradeoffs, and testable where possible.

## Included skills

### `craft-lld-interview-article`

Turns an underspecified low-level design or object-oriented design prompt into an original, interview-sized teaching article with:

- requirements discovery and explicit scope;
- contextual Bad, Good, and Great design comparisons;
- UML-lite Mermaid diagrams;
- a focused class and API design;
- a complete runnable implementation and tests;
- verification, extensions, and level-specific expectations.

The skill is designed around a typical one-hour interview. It favors the smallest design that preserves the important invariants and clearly separates interview implementation from production follow-ups.

### `tailor-tech-job-application`

Builds a research-backed application package for a specific tech role with:

- a cited company context dossier saved before drafting;
- a prioritized job analysis and candidate evidence ledger;
- a concise recruiter email and LinkedIn connection note;
- a contribution-first cover letter;
- a truthful, ATS-readable, one-page tailored resume PDF;
- validation for length, sources, PDF page count, and common AI-writing tells.

The skill uses current first-party and trustworthy independent sources, excludes anonymous employee reviews and social-media rumors, and prevents unsupported keywords or accomplishments from entering the application.

## Install locally

Copy the skill directory into your Codex skills folder:

```bash
cp -R skills/craft-lld-interview-article "$CODEX_HOME/skills/"
cp -R skills/tailor-tech-job-application "$CODEX_HOME/skills/"
```

Restart or reload Codex if needed, then invoke it by name:

```text
Use $craft-lld-interview-article to turn "Design a parking lot" into an article with a runnable Java solution.
Use $tailor-tech-job-application to research this company and tailor my application to the attached tech job description and resume PDF.
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
