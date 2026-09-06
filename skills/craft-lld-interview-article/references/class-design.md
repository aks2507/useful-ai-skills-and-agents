# Class Design Derivation

## The purpose of this section

Class Design is the bridge between requirements and code. It should let the reader watch the object model emerge, class by class. A list of finished method signatures does not provide that bridge.

## Coverage rule

Give every central class its own derivation. A central class is one that owns mutable state, protects an invariant, coordinates a workflow, or supplies a demonstrated behavior boundary.

For each central class, cover:

1. **Responsibility** — one sentence on why the class exists.
2. **State derivation** — map requirements or invariants to fields.
3. **Method derivation** — map caller needs, transitions, or queries to methods.
4. **Interface sketch** — fields and signatures in compact, language-neutral notation.
5. **Invariant** — the rule its methods must preserve.
6. **Knowledge boundary** — what this class should not know.
7. **Collaborators** — direct dependencies and who mutates what.

Use small tables when they expose the derivation. Use prose when a table would have only one obvious row.

## Supporting types

Group types only when none deserves a full lifecycle discussion:

- immutable records;
- semantic identifiers and value types;
- enums;
- exceptions;
- tiny stateless helpers.

Still say what each represents and why it is not a larger class.

## Earn abstractions in sequence

Do not introduce the final inheritance tree or interface set during the noun list. Let the need appear first.

Example sequence:

1. A directory and file both need a name and parent reference.
2. Both participate in path calculation.
3. Callers must traverse them uniformly.
4. A shared `FileSystemEntry` abstraction now removes real duplication and enables a meaningful boundary.

This order makes the abstraction feel inevitable instead of ornamental.

## State test

For every proposed field, ask:

- Is this the source of truth or a cache/index?
- Can it be derived cheaply and unambiguously?
- Does it record a historical outcome that cannot be reconstructed later?
- Is it intrinsic to the object or relational between objects?
- Which operations can change it?

Stored state is justified when it carries physical truth, preserves history, or supports a required atomic claim. Derived state is preferable when it avoids synchronization and remains cheap.

## Method test

For every public method, ask:

- Which requirement or caller need creates it?
- Is it a command, query, or explicit extension boundary?
- Which preconditions are checked?
- Which object is allowed to mutate the relevant state?
- What return value does the caller actually need?

Avoid speculative CRUD, getters for every field, and convenience methods with no article scenario or test.

## Final consolidation

After the per-class derivations, present one Final Class Design. This is the snapshot a candidate could draw on a whiteboard. It must match the code, but it should omit routine constructors, accessors, and incidental implementation detail.
