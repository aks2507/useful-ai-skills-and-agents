# Design Heuristics

## Scope the component

Default to a self-contained, single-process design. Exclude persistence, networking, UI, payments, distributed coordination, and hardware control unless the prompt needs them.

Name excluded production concerns instead of silently ignoring them. Do not implement them until the contract includes them.

## Choose entities deliberately

Retain a class when at least one is true:

- It owns changing state.
- It enforces a domain rule.
- It is a meaningful immutable record created by the component.
- It is the orchestrator for a public workflow.
- It is a stable behavior boundary with real variation.

Keep information as a primitive, enum, or field when it has no independent lifecycle or behavior.

## Identify the orchestrator

Most LLD problems benefit from one public entry point that:

- coordinates a workflow across entities;
- enforces lifecycle-level rules;
- stores relationships between objects;
- hides navigation and lookup details.

Do not turn the orchestrator into a god object. Data-specific rules belong with the object that owns the data.

## Place state using meaning

Ask whether state is intrinsic or relational:

- Intrinsic: physical status, dimensions, identity, local lifecycle.
- Relational: assigned to ticket X, reserved by user Y, membership, lookup mappings.

This is a heuristic, not a law. Defend the selected owner and name the invariant.

When state can be derived, choose among:

1. Compute on demand for one source of truth.
2. Store locally for clearer intrinsic semantics.
3. Maintain an index for justified performance or concurrency.

If duplicating state, document every mutation path that keeps it synchronized.

## Make invalid states difficult to represent

Prefer:

- one enum over several mutually dependent booleans;
- separate semantic types over reusing an enum that admits invalid values;
- validated value objects over ambiguous primitive bundles;
- maps or sets that enforce uniqueness naturally;
- immutable records after creation.

Do not introduce elaborate algebraic types when the chosen language makes them awkward and the interview does not require them. Mention the stronger model and implement the idiomatic one.

## Derive APIs from requirements

Every public method should correspond to a user action, required query, or explicit extension boundary.

Avoid speculative getters, status dashboards, CRUD operations, and configuration mutation. Keep mutation behind a small number of authoritative methods.

Validate closest to the state being protected:

- orchestrator validates workflow and lifecycle;
- collection owner validates membership and bounds;
- value object validates its own construction;
- resource owner validates and mutates atomically.

## Choose data structures from operations

List the dominant operations before selecting a structure:

- lookup by identifier → map;
- uniqueness/membership → set;
- ordered service → queue/deque/ordered set;
- best-next selection → heap or scan depending on N and update cost;
- hierarchical lookup → map of child name to node;
- history/undo → stack of commands or snapshots.

Prefer a simple scan for small bounded N. Explain when an index becomes worthwhile.

## Use composition and inheritance purposefully

Prefer composition when behaviors vary independently, can be swapped, or may be wrapped.

Use inheritance when:

- the subtype relationship is genuine;
- stable behavior and state are shared;
- callers benefit from treating the nodes uniformly;
- the hierarchy is shallow.

Do not create subclasses merely to replace a small parameter or enum.

## Introduce patterns after pressure appears

- Strategy: several interchangeable ways to perform the same policy.
- Factory: construction varies by configuration and should be centralized.
- Observer: the domain emits events to pluggable listeners.
- State: behavior changes materially by lifecycle state.
- Composite: leaf and container nodes share stable tree behavior.
- Facade: callers otherwise repeat internal navigation/workflow.

Naming the pattern is optional. Explaining the requirement and trade-off is mandatory.

## Design concurrency from the guarantee

Do not begin with a lock. Begin with:

1. Shared resource.
2. Required guarantee.
3. Unsafe interleaving.
4. Complete critical section.
5. Lock owner and granularity.

Common guarantees:

- exactly one claimant succeeds;
- a multi-item booking is all-or-nothing;
- a transfer preserves total quantity;
- one record's bytes do not interleave with another's;
- stock never becomes negative;
- reads observe a consistent state.

Start with the simplest correct coarse lock. Move to fine-grained locks only for a stated throughput need.

For multiple locks:

- acquire in deterministic order;
- release in reverse order or a finally/defer construct;
- identify whether locks are reentrant;
- avoid external calls while holding them;
- test opposing acquisition directions.

For check-then-act, protect both the check and mutation in one critical section. A thread-safe collection alone does not make a multi-step invariant atomic.

## Preserve transaction semantics

Validate all inputs and required resources before the first mutation. For multi-object workflows, choose one:

- hold all necessary locks and commit atomically;
- use a staged reservation/commit lifecycle;
- compensate or roll back on failure.

Explain what an observer can see during the operation.

## Calibrate complexity to the level

### Junior

Favor working decomposition, clear state, and the core invariant. Provide hints for advanced algorithms and concurrency.

### Mid-level

Expect clean ownership, idiomatic data structures, useful interfaces, and recognition of common race conditions with limited guidance.

### Senior

Expect proactive counterexamples, atomicity/deadlock reasoning, explicit alternatives, bounded failure behavior, and localized extensions.

## Maintain an interview budget

Target roughly:

- five to nine requirements;
- three to seven central entities;
- one orchestrator;
- two to four core methods;
- one to four comparative decisions;
- zero to two named patterns in the base solution;
- one narrative verification trace;
- two to four extensions.

Exceed these ranges only when the prompt genuinely requires it.
