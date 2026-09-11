# Code That Fits the Interview

The delivered application must be small enough for the candidate to type and explain completely within the stated round. Apply this to every source file, including constructors, helpers, and demo setup. An article that explains three small methods but ships a much larger reference implementation fails this requirement.

## Decide what the program promises

Before coding, separate the inputs into two groups:

- **Setup under our control:** a hardcoded catalog, board dimensions, initial stock, fixed policies, and records created by our own successful operations. State concise assumptions and initialize these directly.
- **Runtime actions:** caller-selected identifiers, coordinates, quantities, payment amounts, and operations whose legality depends on current state. Check the failures that matter to the contract.

This distinction depends on the problem. An administrator editing a catalog through a required API makes catalog fields runtime input. A balance, stock count, or board position can become invalid during ordinary use even when its initial value was hardcoded.

A failed lookup returns no object. Check that result before dereferencing it. A present object can have an invalid field independently of its other fields; skip field validation only because construction is trusted under the stated contract, never because null fields are assumed to occur together.

## Make every guard explain a scenario

For each proposed check, name the permitted caller, the input or action it can supply, and the failure being prevented.

| Origin of the possible failure | Typical decision |
|---|---|
| User chooses an unknown ID, an invalid position, or an unsupported amount | Check at the public operation or immediately after the lookup. |
| Caller acts in the wrong state, funds are insufficient, or a resource is unavailable | Keep the guard; it defines the behavior of the problem. |
| A multi-part operation could change some state and then fail | Check required resources before mutation, at the owner of the rule. |
| A hardcoded object has a blank label, a missing dependency, or an inconsistent internally computed result | Assume correct setup unless validating that data is itself a requirement. |

Use a built-in exception, boolean, or nullable result according to what the caller needs. A domain-specific error hierarchy needs an actual requirement to distinguish failures. Avoid logging, catch-and-rethrow wrappers, retry handling, overflow policies, and detailed error taxonomies unless the prompt puts them in scope.

Place a check where the relevant state is owned. After a collaborator validates its operation, the caller generally handles its result rather than duplicating the collaborator's checks. Rechecking at a later mutation can be justified if the state could have changed; explain that timing distinction.

## Review the rest of the code too

Simplification is broader than deleting exceptions:

- Keep data holders as a few fields or a record with a trivial constructor.
- Store an already-resolved object when storing its ID would only create repeated lookups and helpers. Use IDs when identity, persistence, or changing lookup membership requires them.
- Prefer straightforward loops and standard collections. Choose specialized machinery only when it clarifies a required operation.
- Add a helper when it gives a meaningful rule a name or removes a repeated workflow. Two short statements do not automatically need an abstraction.
- Omit speculative getters, status endpoints, setup validators, builders, factories, and duplicate state.
- Use a small setup example and one short end-to-end call sequence. Do not build a CLI or test framework to demonstrate a handful of methods.
- Preserve useful encapsulation and package boundaries. A single standard-library copy can establish ownership of mutable inventory; an entire validation/copy pipeline for trusted immutable setup usually adds no interview value.

Do not simplify by deleting the main invariant, silently changing required behavior, swallowing errors, or converting explicit logic into dense one-liners.

## Budget the complete implementation

For a 60-minute round that asks for complete code, a useful plan is about 5 minutes for scope, 10 for class design, 30 for typing the application and demo, 5 for verification, and 10 for questions or corrections. Adjust this to the actual prompt and level.

Count and review all application source plus the demo, including routine code. Report the physical line count and which files it includes; optionally also count nonblank lines. The count is evidence of size, not proof of typing speed. Assess how much logic and language ceremony the candidate must explain. Do not impose one universal line limit on games, controllers, and concurrent algorithms.

Read through the entire implementation in the intended typing order. If a junior candidate would need to rush, simplify the contract or representation openly before adding more code. Do not push excess application logic into an appendix, helper module, or a supposedly optional reference version.

Keep focused automated tests as study support. The short demo and a brief manual rejection trace should be enough to demonstrate the solution during the round. Additional tests should prove distinct core behavior or invariants, not enumerate every malformed constructor field. Include them in the PDF so the document remains self-contained.

## Evidence behind this calibration

Reviewed the public pages and Java code tabs on 2026-09-12:

- [Connect Four](https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/connect-four): `Player` stores its name and color directly. `Game` checks turn and terminal state, then delegates placement. The board owns placement validity. Simple return values report rejected moves.
- [Amazon Locker](https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/amazon-locker): `AccessToken` initializes three fields directly. The locker checks lookup failures, expiration, and compartment availability in the operations that use them.
- [Delivery Framework](https://www.hellointerview.com/learn/low-level-design/in-a-hurry/delivery): implementation follows the normal workflow, then the relevant failure paths, followed by a concrete verification trace.
- [Design Principles](https://www.hellointerview.com/learn/low-level-design/in-a-hurry/design-principles): prefer direct solutions and defer features until requirements call for them.

These observations inform the reasoning process. They do not imply that every source example is free of redundant checks. The user's requirement here is stricter than the publisher's common partial-code interview format: our complete application and short demo must be feasible within the round. Preserve original prose, examples, and code.
