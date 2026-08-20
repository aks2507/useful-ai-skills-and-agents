# Comparative Design

## Treat comparisons as small proofs

A comparison should externalize design judgment. It must show why a locally attractive idea is insufficient and how the chosen refinement addresses that exact failure.

Use this loop:

1. **Approach** — describe a design a reasonable candidate could propose.
2. **Appeal** — explain why it looks simple, fast, or well-encapsulated.
3. **Scenario** — run one concrete case against it.
4. **Challenge** — identify the broken requirement, invariant, or cost.
5. **Refinement** — change only the responsible representation, owner, algorithm, or critical section.
6. **Replay** — show how the same scenario behaves now.
7. **Trade-off** — name the new complexity or limitation.
8. **Recommendation** — mark Implement in interview, Mention if asked, or Production extension.

## Meaning of the labels

### Bad

Use Bad only when the approach is plausible but demonstrably wrong for the established contract.

Valid causes include:

- permitting contradictory states;
- losing required information;
- assigning policy to the wrong owner;
- duplicating logic across callers;
- violating atomicity;
- producing unacceptable behavior under a stated workload;
- using a data structure that fails the stated access pattern;
- coupling dimensions that must vary independently.

Do not call an option Bad merely because it violates a named principle or is less extensible.

### Good

Use Good for a correct, explainable design with a known trade-off. Good may be the selected implementation.

Typical Good designs:

- solve the current requirements with the least code;
- use coarse locking that easily meets realistic throughput;
- retain a scan because the collection is small;
- place a simple policy method on the orchestrator;
- use an interface that avoids type branching but leaves minor duplication.

### Great

Use Great for the strongest fit to a specific pressure. State that pressure explicitly.

Great may mean:

- simpler ownership rather than faster asymptotics;
- an enum rather than several flags;
- a maintained index because concurrency needs a claim boundary;
- a richer value object because the primitive loses meaning;
- composition because two dimensions vary independently;
- a multi-resource critical section because atomicity spans both objects.

Great is not synonymous with production-grade, maximum performance, or most patterns.

## Valid comparison shapes

Use whichever shape matches the decision:

- Bad → Great
- Good → Great
- Bad → Good → Great
- Good A ↔ Great B for different objectives
- Several Great alternatives followed by a chosen default
- Great conceptually, Good implemented under the interview time box

Do not manufacture a missing tier.

## Selection rules

After alternatives, write an explicit selection paragraph:

> We will implement X because requirements A and B matter now. Y remains a useful follow-up when condition C becomes true.

Evaluate selection using:

1. Correctness for current requirements.
2. Cognitive load during the interview.
3. Number of mutable sources of truth.
4. Ease of verifying invariants.
5. Actual scale and contention.
6. Likelihood and locality of the stated follow-up.

Prefer the least complex option that fully satisfies the contract.

## High-value comparison families

### State representation

Compare independent booleans or nullable fields against an enum, tagged union, or explicit state object. Count invalid combinations and show one impossible transition.

### State ownership

Compare intrinsic state, derived state, and maintained indexes. State the source of truth and synchronization invariant.

### Public boundary

Compare exposing internal nodes or collections against an orchestrator/facade that centralizes a repeated workflow.

### Data structure

Start from actual operations. Compare list, map, set, queue, heap, or ordered set using the stated lookup and mutation patterns—not generic Big-O trivia.

### Algorithm

Use a stable scenario across algorithms. Evaluate domain outcomes such as fairness, predictability, starvation, or direction changes in addition to total work.

### Abstraction

Compare branching, inheritance, and composition only when behavior varies. An interface needs either multiple current implementations or an explicit pluggable boundary.

### Concurrency

Show the unsafe interleaving. Then compare no synchronization, coarse atomic locking, and fine-grained locking. Name lock ownership, the complete critical section, and deadlock ordering.

### Failure handling

Compare propagation, swallowing, fallback diagnostics, retries, or rollback using the caller's required guarantee.

## Writing the panels

Each panel should contain:

- a descriptive title;
- Approach;
- a small class or method sketch;
- Benefits or initial appeal;
- Challenges or trade-offs;
- recommendation status when the decision is complete.

Keep the counterexample more memorable than the principle name. Prefer one realistic story over five generic bullets.
