# Editorial Calibration Findings

These are generalized teaching patterns distilled from paired analysis of nine representative LLD breakdowns: a board game, locker allocation, elevator control, parking allocation, a file hierarchy, ticket booking, logging, rate limiting, and inventory transfer. They describe functional structure and reasoning habits. They are not a license to copy wording, examples, diagrams, or article-specific composition.

## Stable narrative spine

The most reliable sequence is:

1. A short domain primer.
2. A deliberately brief prompt.
3. Candidate/interviewer clarification that changes the design.
4. Consolidated requirements and explicit exclusions.
5. Candidate-entity filtering and pruning.
6. Per-class state and method derivation.
7. A consolidated design and synchronized diagrams.
8. Deep treatment of the few operations that protect the main invariant.
9. Concrete traces or focused tests.
10. Localized extensions and expectations by candidate level.

The article should feel like a sequence of discoveries. Do not announce a pattern or complete hierarchy before the problem creates the need for it.

## What varied across the nine problems

| Problem pressure | Teaching move that worked |
|---|---|
| Stateful game | Preserve terminal outcomes explicitly when they are historical facts; compare rule-evaluation approaches with a concrete board state. |
| Physical locker allocation | Separate physical occupancy from expiring access credentials; compare allocation policies only after defining fit and availability. |
| Elevator controller | Clarify simulation versus hardware; keep floors as values and earn request/scheduling abstractions through dispatch behavior. |
| Parking allocation | Separate semantic enums even when labels overlap; distinguish spot occupancy, active allocation records, fee calculation, and payment processing. |
| File hierarchy | Keep paths as strings plus focused parsing until shared entry behavior earns a composite abstraction. |
| Seat booking | Treat check-and-reserve as one critical section; derive availability from reservations when the bounded scale makes that clearer. |
| Logging library | Identify formatting and destination as independent variation axes; synchronize the complete sink write rather than a partial step. |
| Rate limiting | Let the workload and guarantees choose the algorithm; use a strategy/factory boundary only because configuration selects behavior. |
| Inventory transfer | Validate before mutation, lock both aggregates in deterministic order, and preserve total quantity across success or failure. |

## Entity pruning patterns

Common non-classes include positions represented by coordinates, floors represented by integers, paths represented by strings plus parsing, fixed seats represented by identifiers, external products represented by product IDs, and request/client/endpoint concepts represented by method parameters or keys.

Rejecting a class is part of the design. State the information that remains and where it lives.

## Comparison calibration

Bad/Good/Great ladders appeared when a problem offered a teachable sequence of refinements, especially for state flags, allocation strategies, scheduling choices, and atomicity. They were absent when a direct algorithm comparison table communicated the decision better.

Therefore:

- require consequential alternative analysis;
- do not require the words Bad, Good, or Great;
- keep the counterexample stable across refinements;
- allow a Good solution to be implemented when the conceptually stronger alternative exceeds the interview budget.

## Semantic checks that transfer well

- Store a value when it represents physical truth or a historical result that later state cannot reconstruct.
- Derive a value when computation is cheap, unambiguous, and removes a second mutable source of truth.
- Name the unit in time and quantity fields.
- Use deterministic tie-breakers in scheduling and allocation.
- Derive return types from the caller's need and the real side effect.
- Separate concepts with different legal values, even if their current labels happen to match.
- Collect external callbacks under a lock only when necessary; invoke them after releasing it.
- For concurrency, name the resource, guarantee, unsafe interleaving, complete critical section, lock owner, and guarantees still not provided.
- State infrastructure failure behavior when an external boundary is in scope.

## Convergence criterion

A generated article is editorially calibrated when:

- its scope is credible for the stated candidate level and time;
- every central class is derived from requirements;
- the main invariant receives the deepest implementation and verification treatment;
- alternatives appear at real pressure points rather than on a fixed schedule;
- diagrams match the code and clarify ownership, lifecycle, or interaction;
- the prose alternates naturally among dialogue, concrete examples, tables, notation, code, and traces;
- no retained concept, method, pattern, or package exists only to make the solution look comprehensive.

Convergence is about these teaching properties, not wording similarity to any source.
