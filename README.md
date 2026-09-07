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

When working inside this repository, Codex discovers the canonical application skill through `.agents/skills`. The repository entry is a symlink to the corresponding directory under `skills/`, so a pull updates the discovered skill without maintaining a second copy.

To use `tailor-tech-job-application` from any working directory, keep the clone and create one global symlink. Replace the example clone path with its absolute path:

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "/absolute/path/to/useful-ai-skills-and-agents/skills/tailor-tech-job-application" "$HOME/.agents/skills/tailor-tech-job-application"
```

Do not keep another copied installation with the same skill name. Codex does not merge same-name skills, so an older copy can remain selectable alongside the current one. Move or disable the old copy before creating the symlink.

Codex automatically detects local skill changes. After pulling an update, invoke the skill again in each active application chat so its freshness gate reads the current version. A dormant chat cannot update until it receives another turn. Restart Codex if the update does not appear. Then invoke it by name:

```text
Use $craft-lld-interview-article to turn "Design a parking lot" into an article with a runnable Java solution.
Use $tailor-tech-job-application to research this company and tailor my application to the attached tech job description and LaTeX resume project.
Use $tailor-tech-job-application to process these three job descriptions separately against the same LaTeX resume project.
```

For resume tailoring, the validator now treats the supplied LaTeX layout as locked. Content-only results must pass locked validation. The format-change override works only with an application-local record quoting the user's explicit request and listing the approved scope.

The application skill also stores its semantic version and instruction digest in every generated application directory. Resuming an application after a skill update triggers a stale-state failure until the current instructions are reread, affected artifacts are reconciled, and current validation passes.

### Updating the application skill

Every change to `tailor-tech-job-application` instructions, references, scripts, or UI metadata must be released as a new skill version:

1. Update the skill files.
2. Bump `skills/tailor-tech-job-application/VERSION` using semantic versioning.
3. Add the new version and its migration implications to `references/version-history.md`.
4. Regenerate the content manifest:

   ```bash
   python3 skills/tailor-tech-job-application/scripts/check_skill_freshness.py --write-manifest
   ```

5. Run the skill tests and `quick_validate.py` before committing.

The manifest command refuses to bless changed content under an unchanged version. A partial pull, manual edit, or stale duplicate is rejected by the skill's freshness gate.

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
    ├── VERSION
    ├── skill-manifest.json
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
