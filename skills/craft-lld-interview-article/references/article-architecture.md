# Article Architecture

## Purpose

Build the article as a guided interview, not a post-hoc description of a finished class diagram. The reader should be able to trace every important design choice back to information discovered earlier.

## Required narrative spine

### 1. Understanding the problem

Give a short domain primer. Explain only the real-world behavior needed to understand the prompt. Avoid historical background and production architecture.

### 2. Requirements

Present the deliberately short interview prompt as a blockquote.

Follow with a candidate/interviewer dialogue. Organize questions around:

1. Core actions.
2. Lifecycle and completion.
3. Errors and illegal operations.
4. Scale or concurrency when it can alter the object model.
5. Scope boundaries.

After an answer, add one or two sentences explaining its design consequence. Use transitions such as:

- this makes the state finite, so an enum is sufficient;
- this separates two independent variation axes;
- this removes payment or networking from the component boundary;
- this turns a check plus mutation into one atomic operation.

Do not ask twenty questions. Ask only questions that narrow the design.

### 3. Final requirements

Write five to nine numbered requirements. Then list four to eight exclusions.

Requirements must be observable behaviors or invariants. Avoid vague items such as "the system should be scalable."

### 4. Core entities and relationships

Walk through the candidate nouns. Explicitly reject at least one tempting entity when appropriate.

Use this test:

- Does it own state that changes?
- Does it enforce a rule?
- Is it a durable record created by this system?
- Does it define an actual axis of variation?

Name the orchestrator and provide a two-column responsibility table. Keep the initial set small enough to hold in working memory.

### 5. Class design

Work top-down from the public entry point. For every central class, answer:

1. What must it remember?
2. What must it do?
3. Which invariants does it own?
4. Which details must it not know?

Use requirement-to-state or requirement-to-method tables for the most important classes. Do not repeat them mechanically for trivial value objects.

Insert comparative design panels at the decision they affect, not in a detached theory section.

### 6. Final class design

Consolidate fields, methods, interfaces, enums, and relationships in language-neutral notation. Follow it with the UML-lite Mermaid diagram when one is warranted.

State the main boundary in one paragraph: who orchestrates, who owns data-specific rules, and where mutation occurs.

### 7. Implementation

Tell the reader which methods are worth implementing in an interview and why. For each central method:

- outline the happy path;
- enumerate edge cases;
- show pseudocode;
- point out delegation and mutation order;
- discuss an alternative only when it changes the trade-off.

Place complete runnable code after the interview implementation, not before it.

### 8. Verification

Trace a scenario with explicit initial state, operations, and resulting state. Include at least one rejected operation or boundary transition.

For transaction or concurrency problems, use multiple focused tests rather than one long trace.

### 9. Extensibility

Add likely "what if" questions. For each:

- identify the requirement change;
- point to the existing seam;
- list the smallest class/API changes;
- state whether existing code remains untouched;
- discuss new correctness obligations.

Stay high level unless the extension itself is the article's central lesson.

### 10. Expectations by level

- Junior: working decomposition, core invariant, and basic edge cases.
- Mid-level: clean ownership, suitable data structures, and limited prompting.
- Senior: proactive counterexamples, trade-offs, concurrency or atomicity where relevant, and localized evolution.

## Pacing for a 60-minute interview

| Segment | Candidate-led time |
|---|---:|
| Requirements | 5–7 min |
| Entities | 3–5 min |
| Class design and comparisons | 12–15 min |
| Core implementation | 15–20 min |
| Verification | 3–5 min |
| Extensions and interviewer discussion | Remaining time |

The article may be longer than the spoken interview. Label what the candidate should implement, mention, or defer.

## Editorial cadence

Alternate among:

- short explanatory paragraphs;
- dialogue;
- compact tables;
- class notation;
- pseudocode;
- diagrams;
- execution traces.

Avoid long abstract lectures. Introduce principles after the concrete decision that demonstrates them.
