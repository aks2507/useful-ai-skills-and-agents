# Quality Rubric

Release an article only when every mandatory gate passes. Use the score to guide revision, not to excuse a failed gate.

## Mandatory gates

### Scope and interview fit

- The time box and candidate level are explicit.
- Requirements and out-of-scope choices are separate.
- The complete application and demo, including constructors and helpers, are credible to type within the interview time box; code size and the proposed time allocation are visible.
- Guards address realistic caller mistakes or required invariants. Trusted setup assumptions are explicit; constructors and downstream helpers do not repeat defensive validation by default.
- Production concerns are clearly labeled rather than silently included.

### Requirement traceability

- Every important requirement maps to an owner and operation.
- Every mutable fact has one authoritative owner or a stated synchronization invariant.
- Every retained class has behavior, changing state, a meaningful record role, or a justified polymorphic boundary.

### Comparative reasoning

- At least one consequential decision is developed through alternatives.
- Any Bad label is supported by a concrete failure, not a slogan.
- Each refinement changes the dimension that caused the failure.
- Tradeoffs and the selected interview implementation are explicit.
- Great means best fit for the current constraints, not most elaborate.
- Bad/Good/Great headings are omitted when a direct option table or counterexample communicates the choice better.

### Design integrity

- Public entry points and invariant owners are clear.
- Every central class has a responsibility, state derivation, method derivation, compact interface, invariant, knowledge boundary, and collaborators.
- Supporting records, enums, and helpers are explained even when grouped.
- Illegal states are prevented, represented explicitly, or rejected consistently.
- Patterns and interfaces are introduced only after their variation pressure appears.
- Concurrency coverage identifies the shared resource and complete critical section when relevant.

### Article and diagram integrity

- The prose follows a question-to-discovery-to-design-to-proof narrative.
- Diagrams teach a non-trivial relationship or transition.
- Diagram names and relationships match the final code.
- The article uses original prose and does not mimic a publisher's wording or distinctive examples.
- Formulaic transitions, repeated contrast templates, empty intensifiers, and monotonous cadence have been revised.

### Implementation integrity

- The solution contains no placeholders or elided logic.
- Source compiles or passes a syntax check.
- Tests cover the core workflow and relevant invalid/lifecycle cases.
- Exact verification commands and honest outcomes are included.
- The narrative walkthrough matches actual behavior.
- Source is grouped into a few meaningful responsibility-based packages or modules.

### Document-bundle integrity

- Markdown and PDF use the question slug and explicit candidate level rather than generic `article` filenames.
- The PDF body is generated from the final Markdown and preserves its section order.
- The PDF appendix contains every production source, test, and required build file with matching checksums.
- Every PDF page has been rendered and visually inspected after the final build.

## Scored review

Score each dimension from 0 to 5:

| Dimension | 5-point standard |
|---|---|
| Interview calibration | Focused, complete, and feasible for the stated level/time |
| Requirement discovery | Questions expose rules and immediately derive consequences |
| Alternative analysis | Concrete failures, minimal refinements, honest tradeoffs |
| Domain model | Few purposeful classes with unambiguous ownership |
| Class derivation | Every central class is traced from requirement to state and method |
| API and state design | Invalid states and mutation boundaries are clear |
| Diagrams | Selective, readable, and synchronized |
| Runnable implementation | Complete, idiomatic, and dependency-light |
| Source organization | Packages teach useful boundaries without framework-like ceremony |
| Verification | Mechanical tests plus a convincing narrative replay |
| Document parity | Named Markdown and PDF agree; the PDF appendix is complete |
| Extension design | Follow-ups remain localized and avoid premature abstraction |
| Editorial quality | Natural pacing, concise transitions, original voice |

Aim for at least 54/65 with no dimension below 3. Mandatory gates still override the numeric score.

## Final red-team pass

Ask:

1. Which class could be removed without losing behavior?
2. Which requirement has no test or walkthrough evidence?
3. Which diagram disagrees with a method or field name?
4. Which “Great” choice is sophisticated but unjustified?
5. Which mutation could leave partial state after failure?
6. Which claim of complexity or thread safety lacks proof?
7. Which paragraph sounds like imitation rather than original teaching?
8. Which central class was presented without showing how its fields and methods were earned?
9. Which package exists only to make the tree look architectural?
10. Does the PDF omit or disagree with any Markdown section or source file?
11. Which em dash, “not X but Y” contrast, or generic transition is doing habitual rather than necessary work?
12. Which guard, helper, accessor, or test exists only to harden trusted setup or support an unrequested behavior?
13. Does the appendix quietly expand the application beyond what the candidate can type and explain?

Revise any positive finding before release.
