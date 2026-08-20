# Implementation and Verification

Treat runnable code as evidence for the design, not as an unrelated appendix.

## Separate interview core from reference completeness

In the article, deeply explain two to four methods that expose ownership, state transitions, validation, or algorithm choice. Put the complete implementation in `solution/`, including routine constructors and accessors needed to run it.

Keep a visible boundary:

- **Implement in interview:** minimum coherent domain model and core flows.
- **Mention if asked:** a localized alternative or extension with a clear seam.
- **Production extension:** infrastructure, distribution, persistence, monitoring, or hardening outside the round.

## Code rules

- Prefer the selected language's standard library.
- Use names from the requirements and diagrams.
- Keep one authoritative owner for each mutable fact.
- Validate all preconditions before the first mutation when failure must be atomic.
- Use domain-specific errors or clearly documented exceptions.
- Inject time, identifiers, and randomness when deterministic tests require control.
- Expose read-only views instead of internal mutable collections.
- Add interfaces only for demonstrated variation or an external boundary.
- Avoid frameworks, dependency injection containers, persistence layers, and build systems unless required.
- Do not include TODOs, omitted branches, placeholder returns, or pseudocode in source files.

## Verification matrix

Cover the smallest useful set of proof cases:

| Concern | Minimum evidence |
|---|---|
| Core workflow | One end-to-end success scenario |
| Invalid input | One rejected action with unchanged state |
| Lifecycle | Transitions plus an operation rejected in the wrong state |
| Boundary | Empty/full/not-found/duplicate case relevant to the prompt |
| Atomicity | No partial update after a failing multi-object operation |
| Concurrency | A repeatable concurrent test when thread safety is in scope |

Do not force irrelevant categories into every solution.

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
