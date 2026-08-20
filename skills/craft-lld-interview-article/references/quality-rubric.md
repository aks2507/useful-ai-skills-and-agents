# Quality Rubric

Release an article only when every mandatory gate passes. Use the score to guide revision, not to excuse a failed gate.

## Mandatory gates

### Scope and interview fit

- The time box and candidate level are explicit.
- Requirements and out-of-scope choices are separate.
- The implemented design is credible within the interview time box.
- Production concerns are clearly labeled rather than silently included.

### Requirement traceability

- Every important requirement maps to an owner and operation.
- Every mutable fact has one authoritative owner or a stated synchronization invariant.
- Every retained class has behavior, changing state, a meaningful record role, or a justified polymorphic boundary.

### Comparative reasoning

- At least one consequential decision is developed through alternatives.
- A Bad label is supported by a concrete failure, not a slogan.
- Each refinement changes the dimension that caused the failure.
- Tradeoffs and the selected interview implementation are explicit.
- Great means best fit for the current constraints, not most elaborate.

### Design integrity

- Public entry points and invariant owners are clear.
- Illegal states are prevented, represented explicitly, or rejected consistently.
- Patterns and interfaces are introduced only after their variation pressure appears.
- Concurrency coverage identifies the shared resource and complete critical section when relevant.

### Article and diagram integrity

- The prose follows a question-to-discovery-to-design-to-proof narrative.
- Diagrams teach a non-trivial relationship or transition.
- Diagram names and relationships match the final code.
- The article uses original prose and does not mimic a publisher's wording or distinctive examples.

### Implementation integrity

- The solution contains no placeholders or elided logic.
- Source compiles or passes a syntax check.
- Tests cover the core workflow and relevant invalid/lifecycle cases.
- Exact verification commands and honest outcomes are included.
- The narrative walkthrough matches actual behavior.

## Scored review

Score each dimension from 0 to 5:

| Dimension | 5-point standard |
|---|---|
| Interview calibration | Focused, complete, and feasible for the stated level/time |
| Requirement discovery | Questions expose rules and immediately derive consequences |
| Alternative analysis | Concrete failures, minimal refinements, honest tradeoffs |
| Domain model | Few purposeful classes with unambiguous ownership |
| API and state design | Invalid states and mutation boundaries are clear |
| Diagrams | Selective, readable, and synchronized |
| Runnable implementation | Complete, idiomatic, and dependency-light |
| Verification | Mechanical tests plus a convincing narrative replay |
| Extension design | Follow-ups remain localized and avoid premature abstraction |
| Editorial quality | Natural pacing, concise transitions, original voice |

Aim for at least 42/50 with no dimension below 3. Mandatory gates still override the numeric score.

## Final red-team pass

Ask:

1. Which class could be removed without losing behavior?
2. Which requirement has no test or walkthrough evidence?
3. Which diagram disagrees with a method or field name?
4. Which “Great” choice is sophisticated but unjustified?
5. Which mutation could leave partial state after failure?
6. Which claim of complexity or thread safety lacks proof?
7. Which paragraph sounds like imitation rather than original teaching?

Revise any positive finding before release.
