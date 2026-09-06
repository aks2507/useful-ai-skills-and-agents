---
name: craft-lld-interview-article
description: Create original, interview-sized low-level design (LLD/OOD) teaching bundles with a question-and-level-named Markdown article, a matching self-contained PDF whose appendix contains the complete codebase, useful UML-lite diagrams, and a sensibly packaged runnable implementation. Use when Codex needs to turn prompts such as "design a parking lot," "design an elevator," "design a logger," or another object-oriented design question into a guided interview solution without overengineering.
---

# Craft LLD Interview Article

Turn an underspecified LLD prompt into an original teaching bundle that shows how a strong candidate discovers a focused solution. Produce an article, a matching PDF, organized source files, tests, and honest verification evidence.

Do not imitate or closely paraphrase a publisher or author. Reuse general teaching techniques, not distinctive wording, examples, analogies, or page composition.

## Load the guidance

Before drafting, read all of these:

- `references/article-architecture.md` for the narrative and section order.
- `references/calibration-findings.md` for the stable patterns learned across nine representative LLD breakdowns.
- `references/comparative-design.md` for contextual design alternatives.
- `references/design-heuristics.md` for scope, ownership, state, APIs, patterns, and concurrency.
- `references/class-design.md` for the required per-class derivation.
- `references/editorial-style.md` for direct, natural prose and the formulaic-writing audit.
- `references/document-bundle.md` for filenames, PDF parity, appendices, and release checks.
- `references/quality-rubric.md` for the release gates.

Additionally:

- Read `references/problem-archetypes.md` after classifying the problem; load only the matching archetype sections.
- Read `references/diagrams.md` before creating diagrams.
- Read `references/implementation-and-verification.md` before writing executable code.
- Read `references/language-profiles.md` for the selected language's source layout and commands.

Use `assets/article-template.md` as a starting structure. For a filesystem artifact, run `scripts/scaffold_article.py`, then replace every scaffold prompt with problem-specific content.

## Normalize the request

Establish:

1. The LLD prompt and domain.
2. Candidate level: junior, mid-level, or senior. If absent, write for mid-level but omit the level from filenames.
3. Time box. Default to a 60-minute round with roughly 45 minutes of candidate-led design and implementation.
4. Implementation language. Honor the user's choice. Otherwise prefer Java when a suitable compiler is available, then Python 3. State the choice.
5. Whether concurrency, persistence, UI, networking, payment, or external hardware is in scope.
6. Desired output location and whether actual files are requested.

Ask only when a missing answer would materially change the design or make a write unsafe. Otherwise state conservative assumptions in the article.

## Execute the workflow

### 1. Establish the interview contract

Open with a short domain primer and the deliberately short prompt. Write a targeted candidate/interviewer dialogue about:

- core actions;
- completion and lifecycle rules;
- invalid actions and error behavior;
- scale and concurrency only when they can alter the design;
- explicit boundaries and likely extensions.

After each meaningful answer, state its immediate design consequence. End with numbered final requirements and a separate out-of-scope list.

### 2. Build traceability before classes

Maintain a private ledger:

`requirement -> owner -> state -> operation -> invariant -> implementation -> verification`

Do not publish the entire ledger unless it helps the reader. Use it to remove speculative classes and methods.

### 3. Identify, classify, and prune candidate entities

Treat nouns as candidates. Classify each useful concept as one of:

- stateful class or orchestrator;
- immutable value or record;
- enum;
- primitive or identifier;
- field or constant;
- behavior boundary with demonstrated variation;
- external concern or rejected concept.

Retain a class only when it owns changing state, enforces rules, represents a meaningful record, coordinates a public workflow, or forms a stable polymorphic boundary. Explicitly explain the non-obvious rejections. Identify one public entry point and the owner of every important invariant.

Do not reveal a shared abstraction before duplicated state, behavior, or typing pressure earns it.

### 4. Select instructive pressure points

Choose one to four decisions that expose real judgment. Favor state representation, ownership, derived versus stored state, public boundaries, data structures, algorithms, independent variation axes, atomicity, or lock granularity.

Comparison ladders are optional. Use them only when two or more plausible choices illuminate a consequential tradeoff.

### 5. Develop contextual alternatives

For each selected comparison:

1. Present a plausible approach and why it initially appeals.
2. Show compact pseudocode or class notation when helpful.
3. Run one concrete counterexample, invariant, or workload against it.
4. Refine only the dimension responsible for the weakness.
5. Replay the same scenario.
6. State the new cost.
7. Mark the choice as **Implement in interview**, **Mention if asked**, or **Production extension**.

Use Bad, Good, and Great only when those labels fit the evidence. Valid shapes include Bad → Great, Good → Great, Bad → Good → Great, an unlabeled option table, and “Great conceptually, Good implemented.” Never manufacture a tier.

### 6. Derive every central class

Start from the public entry point, then move to collaborators. For every central class, include:

1. responsibility and reason to exist;
2. requirement-to-state table;
3. requirement-or-caller-need-to-method table;
4. compact interface sketch;
5. owned invariant and knowledge boundary;
6. collaborators and mutation responsibility.

Compact records, enums, exceptions, and helpers may share a grouped subsection. Do not reduce Class Design to an explanation of the orchestrator.

Resolve abstractions during this derivation when the repeated shape becomes visible. Follow with one consolidated Final Class Design.

### 7. Draw the smallest useful model

Include a synchronized UML-lite class diagram for the final non-trivial design. Add a state, sequence, data-structure, or race diagram only when it materially shortens the explanation.

Keep names identical across prose, diagrams, and code. A simple junior solution may need only the class diagram and one small state diagram.

### 8. Implement the interview core

Choose two to four methods that reveal the design. For each:

1. Explain the happy path.
2. List relevant invalid states and edge cases.
3. Validate before mutating.
4. Show explicit pseudocode.
5. Explain delegation and mutation order.

Give the highest-invariant operation the most attention. Say why routine constructors, accessors, and mechanical helpers are skipped in the narrative.

### 9. Create the organized runnable solution

Create complete source and tests under `solution/` using the selected language layout in `references/language-profiles.md`.

Organize by responsibility and dependency direction, not by file count. Typical packages are `model`, `service`, and a demonstrated `policy` boundary. Keep closely related tiny types together where the language permits. Do not create a package for every class, a catch-all `utils` package, or a framework-like layer with one file in each directory.

Include a deterministic demo and focused tests for the core workflow, invalid input, lifecycle transitions, and applicable atomicity or concurrency guarantees. Do not leave placeholders or elided branches.

Compile and run the implementation. Fix failures before calling it complete.

### 10. Build the paired documents

Name the Markdown file after the question, adding the explicitly requested level:

- `vending-machine-junior.md`
- `parking-lot.md` when no level was specified.

Build a PDF with the identical stem. The PDF body must be generated from the final Markdown, not from a separately edited summary. Append every source, test, and required build file under **Appendix: Complete Runnable Code** so the PDF alone is enough to study and run the solution.

Run:

```bash
python3 scripts/build_pdf.py path/to/question-level.md \
  --solution-dir path/to/solution
```

Use the bundled PDF Python runtime when available. Render the resulting PDF to images, inspect every page for clipping, overflow, unreadable diagrams, orphaned headings, and appendix code loss, then revise and rebuild if necessary.

### 11. Verify narratively and mechanically

Walk through one concrete scenario from initial state to completion or rejection. For concurrency, show an unsafe interleaving before the fix and a targeted test afterward.

Run the solution's exact compile, test, and demo commands. Then run:

```bash
python3 scripts/validate_article.py path/to/question-level.md \
  --solution-dir path/to/solution \
  --pdf path/to/question-level.pdf
```

When the user explicitly supplied a level, also pass `--candidate-level junior`, `--candidate-level mid-level`, or `--candidate-level senior` so filename validation is strict.

Apply `references/quality-rubric.md`, including the prose audit. Revise until every mandatory gate passes.

### 12. Finish with extensions and level expectations

Add two to four likely interviewer follow-ups. Describe localized changes rather than rewriting the system.

End with junior, mid-level, and senior expectations for the same problem. Give special emphasis to the requested level.

## Output contract

When creating files, return:

```text
<problem-slug>/
├── <problem-slug>[-<level>].md
├── <problem-slug>[-<level>].pdf
└── solution/
    ├── src/                 # language-appropriate packages beneath this
    ├── tests/ or src/test/  # language-appropriate test root
    └── build metadata only when required
```

The Markdown must point to real source files and include exact commands. The PDF must present the same article and contain the full runnable code appendix. Clearly separate interview implementation, mention-only ideas, and production extensions.

For text-only requests, still provide complete code blocks and state that they were not executed unless a runnable workspace was available. A PDF is mandatory only when creating filesystem artifacts.

## Non-negotiable constraints

- Keep the problem self-contained unless distributed behavior is explicitly requested.
- Do not turn every noun into a class.
- Do not introduce a pattern before showing the pressure it solves.
- Do not call a design Bad without a concrete failure.
- Do not require a Bad/Good/Great ladder in every article.
- Do not equate Great with maximum abstraction or performance.
- Do not duplicate mutable state without a named synchronization invariant.
- Do not discuss thread safety without the shared resource and complete critical section.
- Do not call code complete until it compiles/runs and tests pass.
- Do not maintain Markdown and PDF prose independently.
- Do not use `article.md` or `article.pdf` as final filenames.
- Do not ship a flat multi-class source dump when meaningful package boundaries exist.
- Do not use prose-pattern randomization or claim to evade AI detectors; write precise, original prose and remove repetitive templates.
