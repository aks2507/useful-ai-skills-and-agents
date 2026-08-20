---
name: craft-lld-interview-article
description: Create original, interview-sized low-level design (LLD/OOD) problem breakdowns that narrate requirements discovery, compare bad/good/great design alternatives, derive classes and behavior, add UML-lite Mermaid diagrams, and include a complete runnable implementation with verification. Use when Codex needs to turn prompts such as "design a parking lot," "design an elevator," "design a logger," or another object-oriented design question into a polished teaching article, worked interview solution, or executable reference project without overengineering.
---

# Craft LLD Interview Article

Turn an underspecified LLD prompt into an original teaching article that demonstrates how a strong candidate discovers an appropriately scoped solution. Produce both the article and executable source files.

Do not imitate or closely paraphrase a particular publisher or author. Apply the general editorial techniques in this skill using original prose.

## Load the guidance

Before drafting, read:

- `references/article-architecture.md` for the required narrative and section order.
- `references/comparative-design.md` for bad/good/great decision progressions.
- `references/design-heuristics.md` for scope, ownership, state, APIs, patterns, and concurrency.
- `references/quality-rubric.md` for the release gates.

Additionally:

- Read `references/problem-archetypes.md` after classifying the problem; load only the matching archetype sections.
- Read `references/diagrams.md` before creating Mermaid diagrams.
- Read `references/implementation-and-verification.md` before writing executable code.
- Read `references/language-profiles.md` for the selected language's project layout and verification commands.

Use `assets/article-template.md` as a starting structure when creating a new artifact. Run `scripts/scaffold_article.py` when a filesystem artifact is requested.

## Normalize the request

Establish:

1. The LLD prompt and domain.
2. Candidate level: junior, mid-level, or senior.
3. Time box. Default to a 60-minute round with roughly 45 minutes of candidate-led design and implementation.
4. Implementation language. Honor the user's choice. Otherwise prefer Java when a suitable compiler is available, then Python 3 as the portable fallback. State the choice.
5. Whether concurrency, persistence, UI, networking, or external hardware is in scope.
6. Desired output location and whether to create actual files.

Ask a question only when a missing answer would materially change the design or cause an unsafe write. Otherwise make conservative assumptions and display them in the article.

## Execute the workflow

### 1. Establish the interview contract

Start from the short prompt. Write a realistic candidate/interviewer clarification dialogue covering:

- core actions;
- completion and lifecycle rules;
- invalid actions and error behavior;
- scale and concurrency only when relevant;
- explicit boundaries and likely extensions.

After each meaningful answer, explain its immediate design consequence. Conclude with numbered requirements and a separate out-of-scope list.

### 2. Build traceability before classes

Create a private working ledger:

`requirement -> owner -> state -> operation -> invariant -> implementation -> verification`

Do not publish the full ledger unless it improves the article. Use it to ensure every class and method is earned.

### 3. Identify and prune entities

Consider nouns as candidates, not automatic classes. Retain an entity only when it owns changing state, enforces rules, represents a meaningful domain record, or forms a stable polymorphic boundary.

Identify one public entry point or orchestrator. State which class owns each important invariant. Present a concise responsibility table.

### 4. Select instructive design pressure points

Choose one to four decisions that expose real judgment. Favor:

- state representation;
- state ownership or indexing;
- public boundaries;
- data structures;
- algorithms;
- independent variation axes;
- atomicity or lock granularity.

Do not force every decision into a comparison.

### 5. Develop contextual alternatives

For each selected pressure point:

1. Present a plausible approach and its appeal.
2. Show compact pseudocode or class notation.
3. Demonstrate a concrete counterexample, invariant violation, or workload.
4. Refine only the dimension responsible for the weakness.
5. Replay the scenario.
6. State the new cost.
7. Mark the outcome as **Implement in interview**, **Mention if asked**, or **Production extension**.

Treat Bad, Good, and Great as contextual labels. Great does not mean most sophisticated. A Good design may be the correct implementation when a Great alternative is outside the time box or current scope.

### 6. Derive the class design top-down

Start with the orchestrator. For each class, derive:

- state from requirements and invariants;
- behavior from supported actions and queries;
- collaborators from ownership boundaries;
- visibility from the smallest necessary public API.

Prefer compact code-shaped notation over formal UML prose. Then show a single consolidated Final Class Design.

### 7. Add the smallest useful diagrams

Generate Mermaid diagrams that teach relationships the prose cannot express as efficiently:

- a UML-lite class diagram for non-trivial ownership or polymorphism;
- a state diagram for lifecycle-driven behavior;
- a sequence diagram for a multi-object workflow;
- a race/interleaving diagram for concurrency bugs.

Keep the diagram synchronized with the final class design and runnable code. Do not add a diagram merely to decorate the article.

### 8. Implement the interview core

Choose two to four methods that reveal the design. For each:

1. Explain the happy path.
2. List edge cases and illegal states.
3. Validate before mutating.
4. Show explicit pseudocode.
5. Explain delegation and mutation order.

Keep advanced alternatives out of the base implementation unless the selected requirements justify them.

### 9. Create the runnable reference solution

Create actual source and test files under `solution/`. Use the standard library first. Include a deterministic entry point or demonstration and tests for the core workflow, invalid input, lifecycle transitions, and applicable concurrency/atomicity guarantees.

Inject clocks, identifiers, or randomness when they otherwise make tests nondeterministic. Do not leave placeholders, elided methods, or "exercise for the reader" gaps.

Compile and run the implementation. Fix failures before presenting it as complete.

### 10. Verify narratively and mechanically

In the article, walk through one concise but non-trivial scenario from initial state to completion or failure. For concurrency, show an unsafe interleaving before the fix and a targeted concurrent test after it.

Run:

```bash
python3 scripts/validate_article.py path/to/article.md --solution-dir path/to/solution
```

Then apply `references/quality-rubric.md`. Revise until all mandatory gates pass.

### 11. Finish with extensions and level expectations

Add two to four likely interviewer follow-ups. Explain localized changes rather than rewriting the system.

End with separate junior, mid-level, and senior expectations calibrated to the same base problem.

## Output contract

When creating files, return:

```text
<problem-slug>/
├── article.md
└── solution/
    ├── source files
    ├── tests
    └── build metadata only when required by the language
```

The article must link or refer to the real source files, include exact run commands, and clearly separate the interview-sized implementation from optional production extensions.

When the user requests text only, still provide complete code blocks and state that they were not executed unless a runnable workspace was available.

## Non-negotiable constraints

- Keep the problem self-contained unless distributed behavior is explicitly requested.
- Do not turn every noun into a class.
- Do not introduce a design pattern before showing the pressure it solves.
- Do not claim a design is Bad only by naming a principle; demonstrate the failure.
- Do not equate Great with maximum abstraction or theoretical performance.
- Do not duplicate mutable state without naming the synchronization invariant.
- Do not discuss thread safety without identifying the shared resource and complete critical section.
- Do not call code complete until it compiles/runs and its tests pass.
- Use original prose and examples.
