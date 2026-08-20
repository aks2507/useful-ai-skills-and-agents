# Problem Archetypes

Classify the prompt by its dominant design pressure. A problem can match more than one archetype, but choose one primary archetype so the article has a clear spine.

## Stateful game or rules engine

Examples: tic-tac-toe, chess clock, card game, bowling.

- Center the model on turns, legal actions, phase transitions, and terminal conditions.
- Typical owners: `Game` or `Match` orchestrator, `Board` or aggregate state, immutable `Move`, optional rule strategy.
- Core invariant: only legal actions advance the game, and a terminal game cannot advance.
- Useful comparison: scattered booleans versus one explicit state/phase; rule logic inside pieces versus a cohesive rule owner.
- Useful diagrams: state diagram plus a small class diagram.
- Common excess: modeling every physical concept, networking, matchmaking, spectators, or persistence.

## Simulation or controller

Examples: elevator, traffic light, coffee machine, vending machine.

- Separate accepted commands from physical or logical state transitions.
- Typical owners: controller/orchestrator, controlled unit, request or command, selection policy when justified.
- Core invariant: commands may cause only valid transitions, and the controller has one authoritative view of unit state.
- Useful comparison: direct callers mutating units versus controller-mediated operations; one boolean per condition versus an explicit state model.
- Useful diagrams: state diagram and one end-to-end sequence.
- Common excess: real hardware protocols, distributed dispatch, telemetry pipelines, or predictive scheduling.

## Resource allocation

Examples: parking lot, meeting rooms, lockers, seat assignment.

- Make availability, eligibility, allocation, and release explicit.
- Typical owners: facility or service orchestrator, resource, allocation record, selection policy if multiple strategies matter.
- Core invariant: a resource has at most one active allocation and release affects the exact allocation that acquired it.
- Useful comparison: linear scan versus maintained availability index; resource-only occupancy flag versus allocation record with identity and lifecycle.
- Useful diagrams: class diagram and allocate/release sequence.
- Common excess: distributed inventory, payment systems, database schemas, or reservation markets unless requested.

## Hierarchy or composite

Examples: file system, organization chart, menu tree, package structure.

- Focus on parent/child ownership, traversal, naming, and cycle prevention.
- Typical owners: node abstraction, leaf, container/composite, optional traversal service.
- Core invariant: the structure remains acyclic and a child has the allowed number of parents.
- Useful comparison: caller-side type checks versus polymorphic operations; mutable child lists exposed publicly versus controlled mutations.
- Useful diagrams: class diagram and a small object/tree example.
- Common excess: permissions, remote synchronization, full query languages, or persistence.

## Booking or reservation lifecycle

Examples: hotel rooms, movie tickets, appointments, vehicle rentals.

- Distinguish temporary holds, confirmed bookings, cancellation, and expiration only when the prompt needs them.
- Typical owners: booking service, resource/calendar, reservation record, clock abstraction for expiration.
- Core invariant: overlapping active reservations cannot claim the same capacity.
- Useful comparison: check-then-write versus atomic reserve; deriving availability from reservations versus duplicating availability flags.
- Useful diagrams: reservation state diagram and concurrent booking sequence.
- Common excess: payments, notifications, identity platforms, or distributed transactions.

## Pluggable library or policy engine

Examples: logger, rate limiter, notification dispatcher, pricing engine.

- Identify independent variation axes before introducing interfaces.
- Typical owners: facade, immutable input/event, one interface per real variation axis, concrete strategies or sinks.
- Core invariant: policy selection and side effects remain explicit and independently testable.
- Useful comparison: conditionals mixed with effects versus policy plus sink; inheritance across unrelated axes versus composition.
- Useful diagrams: class diagram; sequence only if the pipeline is non-obvious.
- Common excess: plugin discovery, reflection, configuration servers, async queues, or retry platforms.

## Stateful algorithm container

Examples: LRU cache, in-memory key-value store, leaderboard, browser history.

- Derive the data structure from required operation complexity and update coupling.
- Typical owners: one container, internal node/entry record, optional eviction or ranking policy.
- Core invariant: all internal representations describe the same logical contents.
- Useful comparison: a simple scan versus an index; duplicated structures updated independently versus one atomic mutation path.
- Useful diagrams: object/data-structure sketch expressed as Mermaid flowchart or class diagram.
- Common excess: unnecessary domain classes, persistence, sharding, or generic frameworks.

## Inventory or transfer workflow

Examples: wallet transfer, warehouse inventory, library loans, order fulfillment.

- Model quantity or ownership changes as a guarded operation with a record of what occurred.
- Typical owners: service/orchestrator, account or stock aggregate, transfer/loan record, optional repository boundary.
- Core invariant: conservation holds and a failed operation has no partial mutation.
- Useful comparison: sequential independent updates versus one transaction boundary; mutable totals in several places versus a single source of truth.
- Useful diagrams: operation sequence and lifecycle diagram when records change state.
- Common excess: ledgers, reconciliation jobs, event buses, or distributed consensus unless explicitly in scope.

## Selecting the article's pressure points

For the primary archetype, choose the invariant and one comparison listed above. Add a second archetype only when a requirement genuinely introduces another pressure. Keep the base solution recognizable as something a candidate can explain and partially implement within the stated time box.
