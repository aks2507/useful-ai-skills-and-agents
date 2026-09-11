# Implementation and Verification

Treat runnable code as evidence for the design. It is organized as a reference project on disk and reproduced completely in the PDF appendix.

## One complete interview implementation

In the article, deeply explain two to four methods that expose ownership, state transitions, validation, or algorithm choice. Put that same implementation in `solution/`, with only the routine code needed to compile and run it. Apply `interview-code-budget.md` to every source file; a richer reference version in the appendix does not satisfy the typing budget.

Organize the project into a few meaningful packages or modules before writing files. Use dependency direction to choose boundaries: domain values and entities should not depend on orchestration, while optional policies may be injected into the service that uses them.

Keep a visible scope boundary:

- **Implement in interview:** minimum coherent domain model and core flows.
- **Mention if asked:** a localized alternative or extension with a clear seam.
- **Production extension:** infrastructure, distribution, persistence, monitoring, or hardening outside the round.

## Code rules

- Prefer the selected language's standard library.
- Use names from the requirements and diagrams.
- Keep one authoritative owner for each mutable fact.
- Check relevant runtime preconditions before the first mutation when failure must be atomic. Trust the explicitly stated setup assumptions.
- Use simple return values or built-in exceptions; add error types only when callers need to distinguish them.
- Inject time, identifiers, and randomness when deterministic tests require control.
- Keep mutable state behind its owner. Add a collection view only when a caller needs it; trust fixed demo data rather than adding layers of defensive copies.
- Add interfaces only for demonstrated variation or an external boundary.
- Avoid frameworks, dependency injection containers, persistence layers, and build systems unless required.
- Avoid a flat source dump when four or more production types have clear model, service, or policy responsibilities.
- Avoid artificial packages containing one incidental class; closely related small types may share a package or source file when idiomatic.
- Do not include TODOs, omitted branches, placeholder returns, or pseudocode in source files.

## PDF appendix

After verification, generate the PDF from the final Markdown and the complete `solution/` tree. Include production code, tests, and required build metadata. The appendix manifest records each relative path and SHA-256 checksum so `validate_article.py` can detect drift.

## Verification matrix

Cover the smallest useful set of proof cases. These are possibilities to select from, not a checklist requiring a separate test for each row. Keep additional tests separate from the short interview demo:

| Concern | Minimum evidence |
|---|---|
| Core workflow | One end-to-end success scenario |
| Invalid input | One realistic caller mistake with unchanged state |
| Lifecycle | Transitions plus an operation rejected in the wrong state |
| Boundary | A runtime empty/full/not-found case that demonstrates a required rule |
| Atomicity | No partial update after a failing multi-object operation |
| Concurrency | A repeatable concurrent test when thread safety is in scope |

Do not force irrelevant categories into every solution or test malformed hardcoded configuration. Prioritize failures that could corrupt the main state transition.

## Mechanical verification

Run from the generated problem directory. Record exact commands and outcomes in the article.

1. Format or statically check only when the required tool is already available.
2. Compile or syntax-check all source files.
3. Run the complete test suite.
4. Run the deterministic demonstration if one is supplied.
5. Re-run after any article-driven code correction.

Never state that code passes if commands were not executed. If execution is unavailable, label the code unverified and give the reader exact commands.

## Narrative verification

Walk through one scenario using concrete identifiers and state values. At each step, name:

- the public call;
- the object that validates it;
- the state read;
- the mutation performed;
- the invariant preserved;
- the returned result or error.

This replay should connect requirements, design, and code without introducing a new abstraction.

## Concurrency

Add concurrency only when the same mutable resource can be touched by multiple callers within scope. Identify:

1. The shared resource.
2. The unsafe read/check/write interleaving.
3. The complete critical section.
4. The chosen lock or atomic primitive and its granularity.
5. The throughput or complexity tradeoff.
6. A targeted test that would expose duplicate allocation, lost updates, or partial transfers.

Do not claim general thread safety when only one method or data structure has been protected.
