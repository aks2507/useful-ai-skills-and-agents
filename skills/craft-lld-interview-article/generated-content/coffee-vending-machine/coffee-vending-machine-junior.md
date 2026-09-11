# Design Coffee Vending Machine

> **Interview frame:** 60 minutes · junior candidate · Java 25

## Understanding the Problem

A coffee vending machine offers a small menu, collects money, checks whether the selected drink can be prepared, consumes its recipe, and returns change. The interesting part of the interview is the order of those steps. An unsuccessful purchase must leave both the customer's money and the ingredient stock in a sensible state.

> **Prompt:** Design a coffee vending machine that lets a customer select a drink, insert coins, dispense it, receive change, or cancel the purchase.

### Clarifying Questions

**Candidate:** Which drinks and ingredients should the machine support?

**Interviewer:** Configure the menu when the machine starts. For this exercise, recipes use water in millilitres, coffee in grams, and milk in millilitres.

The menu should contain data rather than recipe-specific branches. `Ingredient` can be an enum because the set is closed for this round. Each recipe maps an ingredient to the required integer amount.

**Candidate:** Are drink customizations such as extra shots or sugar required?

**Interviewer:** No. Each menu entry has one fixed recipe and price.

One `Beverage` record can carry the code, display name, price, and recipe. The demo creates fixed recipes with `Map.of`.

**Candidate:** How does payment work?

**Interviewer:** Accept coins worth 25, 50, 100, or 200 cents. Prices and balances use integer cents. Assume the machine can always return the calculated change.

This removes floating-point rounding and physical change-coin inventory from the base design. The completed result only needs the amount of change.

**Candidate:** Can money be inserted before a drink is selected?

**Interviewer:** Keep one simple order: select, insert coins, then dispense. The customer may cancel at any point before dispensing.

The machine needs one active selection and one balance. It rejects a second selection until the current session finishes or is cancelled.

**Candidate:** Is brewing asynchronous, and can several customers use the same instance at once?

**Interviewer:** No. Treat preparation as a synchronous simulation for one customer.

We can return the completed drink from `dispense()`. Motor control, brewing progress, timers, and locks would distract from the junior-level object model.

### Final Requirements

1. Use the menu configured at startup to look up drinks by code.
2. Store a fixed price and ingredient recipe for each beverage.
3. Select one known beverage only when its recipe is currently available.
4. Accept only 25, 50, 100, and 200 cent coins after a selection.
5. Dispense after the inserted balance covers the selected price.
6. Consume every recipe ingredient exactly once on a successful dispense.
7. Return the beverage, total paid, and calculated change, then clear the session.
8. Cancel a purchase, return the inserted balance, and consume no ingredients.
9. Reject invalid operation order, unsupported coins, insufficient payment, or insufficient ingredients without partial ingredient consumption.

### Out of Scope

- heaters, grinders, pumps, sensors, and physical failure handling;
- card authorization and payment settlement;
- tracking the denominations available for change;
- custom drink sizes, extra shots, sugar, or temperature choices;
- administrator authentication and restocking operations;
- persistence, networking, telemetry, and concurrent customers.

### Setup Assumptions

The demo supplies a valid menu with unique codes, positive prices and recipe amounts, and non-negative starting stock. Recipes are fixed `Map.of` values. These are setup assumptions, so constructors simply store the data they receive.

Customer actions still need checks: a code may not be on the menu, a coin may be unsupported, or the customer may try to dispense too early. Ingredient stock can also be insufficient. Those cases affect the purchase workflow and belong in the implementation.

## Finding the Core Entities

Some familiar coffee-machine concepts do not earn classes in this contract. A grinder and brewer matter to physical hardware, but the simulation has one synchronous `dispense()` operation. A customer supplies commands and has no stored identity. Coins have no behavior beyond membership in a fixed set of accepted integer values.

| Candidate | Keep as | Reason |
|---|---|---|
| Coffee vending machine | Class | Coordinates the menu, customer session, payment checks, and preparation. |
| Ingredient inventory | Class | Owns mutable quantities and the all-or-nothing consumption rule. |
| Beverage | Record | Carries fixed menu data and a recipe. |
| Dispense result | Immutable record | Preserves the completed purchase after the machine resets. |
| Ingredient | Enum | Defines the closed ingredient keys and embeds measurement units in their names. |
| Coin | Integer plus a set | Four fixed values need validation, not an object lifecycle. |
| Customer | Reject | Identity does not affect any requirement. |
| Brewer and grinder | Reject for the base | Hardware execution is outside the synchronous simulation. |

### Responsibilities at a Glance

| Type | Responsibility | State or invariant owned |
|---|---|---|
| `CoffeeVendingMachine` | Public purchase workflow | At most one selected beverage and its balance. |
| `IngredientInventory` | Check and consume recipes | Quantities stay non-negative; failed consumption changes nothing. |
| `Beverage` | Describe one menu option | Trusted code, name, price, and fixed recipe. |
| `DispenseResult` | Report one completed purchase | Values computed by the successful dispense. |
| `Ingredient` | Give ingredient quantities semantic keys | Each enum name includes its measurement unit. |

## Exploring the Design

### Decision: where should recipe consumption live?

Consider a latte that needs 40 ml of water, 18 g of coffee, and 120 ml of milk. The inventory currently has exactly enough water and coffee but only 100 ml of milk.

#### Bad: decrement ingredients while checking them

A direct implementation inside `dispense()` may look compact:

```text
waterMl -= 40
coffeeGrams -= 18
if milkMl < 120: reject
milkMl -= 120
```

The rejection arrives too late. Water and coffee have already been removed even though no latte was produced. The operation broke the requirement that failure preserve the inventory.

#### Good: validate the full recipe first

The machine can make two passes: first check every amount, then perform every decrement.

```text
require waterMl >= 40
require coffeeGrams >= 18
require milkMl >= 120

waterMl -= 40
coffeeGrams -= 18
milkMl -= 120
```

This is correct for one drink, but each new recipe adds another branch to the purchase orchestrator. The class that manages payment would also know every ingredient field.

#### Great for this scope: let the inventory consume a recipe

Represent a recipe as `Map<Ingredient, Integer>`. `IngredientInventory.consume(recipe)` checks that stock covers every recipe entry in one pass and mutates quantities in a second pass. The same operation prepares espresso or latte without changing the machine workflow.

The map adds a small amount of indirection, but it keeps one stock owner and one mutation path. A junior candidate can explain and code both loops within the interview.

**Recommendation:** **Implement in interview.** Keep the generic two-pass consumption method. **Mention if asked:** a richer unit type could prevent mixing grams and millilitres in a larger model.

### Decision: should the machine store an explicit state enum?

An enum with `IDLE`, `SELECTED`, and `READY` seems natural. `READY`, however, depends on the selected beverage's price and the current balance. Every accepted coin could require an extra state update.

The selected beverage and balance already contain the needed facts:

- no selected beverage means the machine is idle;
- a selected beverage means coins may be inserted;
- `balanceCents >= beverage.priceCents()` means dispensing has enough money.

Deriving these conditions avoids a second mutable representation. Each public method still checks whether its transition is legal.

**Recommendation:** **Implement in interview.** Use the two fields. **Production extension:** introduce explicit brewing states when hardware reports asynchronous progress or failure.

## Class Design

### `CoffeeVendingMachine`: purchase orchestrator

`CoffeeVendingMachine` is the only public workflow entry point. It resolves menu codes, enforces operation order, tracks the current payment, and asks the inventory to consume the selected recipe. It does not know how individual ingredient quantities are stored or changed.

| Requirement or invariant | State needed | Why this owner |
|---|---|---|
| Resolve a configured drink | `menuByCode` | The machine owns its selectable menu boundary. |
| Allow one active purchase | `selected` beverage | Retains the menu object resolved at selection. |
| Accumulate inserted money | `balanceCents` | Balance spans coin insertions, cancellation, and dispensing. |
| Validate denominations | `SUPPORTED_COINS` | Coin acceptance belongs at the public input boundary. |
| Prepare the selected recipe | `inventory` collaborator | Ingredient mutation belongs to its dedicated owner. |

| Caller need or transition | Method | Result or mutation |
|---|---|---|
| Start a purchase | `select(code)` | Stores one known, available beverage. |
| Add payment | `insertCoin(cents)` | Validates and increases the active balance. |
| Finish a purchase | `dispense()` | Consumes one recipe, resets the session, and returns the result. |
| Abandon a purchase | `cancel()` | Clears the session and returns the balance. |

```text
class CoffeeVendingMachine
  menuByCode: Map<String, Beverage>
  inventory: IngredientInventory
  selected: Beverage?
  balanceCents: int

  select(code): void
  insertCoin(cents): void
  dispense(): DispenseResult
  cancel(): int
```

**Invariant:** A completed dispense consumes one whole recipe and clears the session. A rejected operation cannot partially consume a recipe.

**Knowledge boundary:** The machine knows recipe requirements through `Beverage`, but it does not access or decrement ingredient fields itself.

**Collaborators:** It reads `Beverage` menu data, delegates stock checks and consumption to `IngredientInventory`, and creates `DispenseResult`.

Keeping the selected object makes its price and recipe available directly. The menu stays fixed during a purchase, so storing only the code would add a lookup with no useful behavior. The private `clearSession()` helper resets the two fields used by both cancellation and dispensing.

### `IngredientInventory`: ingredient stock owner

`IngredientInventory` stores the physical ingredient quantities. It is the only class allowed to decrement them. Each operation visits the recipe entries; an ingredient absent from stock has quantity zero. The constructor copies the starting quantities into its own map so the inventory can mutate them.

| Requirement or invariant | State needed | Why this owner |
|---|---|---|
| Track all current quantities | `quantities` enum map | One map is the ingredient source of truth. |
| Decide recipe availability | recipe input plus quantities | The answer depends only on inventory data. |
| Prevent partial consumption | two-pass operation | All amounts are checked before the first decrement. |

| Caller need or transition | Method | Result or mutation |
|---|---|---|
| Check menu availability | `canPrepare(recipe)` | Returns whether every required amount is present. |
| Prepare one drink | `consume(recipe)` | Rejects without mutation or decrements the complete recipe. |
| Inspect deterministic state | `quantityOf(ingredient)` | Supports the demo and correctness tests. |

```text
class IngredientInventory
  quantities: Map<Ingredient, Integer>

  canPrepare(recipe): boolean
  consume(recipe): void
  quantityOf(ingredient): int
```

**Invariant:** Starting from the valid setup, quantities stay non-negative. If one recipe requirement cannot be met, all quantities retain their previous values. The order of the map entries does not affect this guarantee.

**Knowledge boundary:** The inventory understands ingredient amounts, not menu codes, prices, coins, or customer-session order.

**Collaborators:** It receives immutable recipe maps from a `Beverage`; only `CoffeeVendingMachine` calls it during a purchase.

### `Beverage`: fixed menu entry

`Beverage` represents the stable information needed after a code is selected. A Java record supplies its constructor and accessors. The recipe is already immutable because the demo uses `Map.of`; the record adds no validation or copying.

| Requirement or invariant | State needed | Why this owner |
|---|---|---|
| Select by a compact value | `code` | The code identifies the menu entry. |
| Display the chosen drink | `name` | The completed result needs a readable name. |
| Check payment | `priceCents` | Price belongs to the menu entry and uses an explicit unit. |
| Consume ingredients | `recipe` | The fixed recipe defines the beverage. |

| Caller need or transition | Method | Result or mutation |
|---|---|---|
| Configure a drink | record constructor | Stores the supplied demo values. |
| Read menu data | record accessors | Exposes the fixed fields and recipe. |

```text
record Beverage
  code: String
  name: String
  priceCents: int
  recipe: Map<Ingredient, Integer>
```

**Setup contract:** Prices and recipe amounts are positive, and the demo passes immutable recipe maps. A record alone does not make a mutable map immutable; this property comes from how the demo constructs it.

**Knowledge boundary:** A beverage does not know inventory quantities, payment state, or preparation order.

**Collaborators:** The machine indexes it; the inventory reads its recipe.

### `DispenseResult` and `Ingredient`: supporting values

`DispenseResult` is an immutable snapshot of a successful purchase. The machine clears its session before accepting another customer, so returning a record keeps the finished values available to the caller. `Ingredient` supplies semantic recipe keys. Its constants include units, such as `WATER_ML` and `COFFEE_GRAMS`, which prevents an unlabeled amount from crossing the API.

| Requirement or invariant | State needed | Why this owner |
|---|---|---|
| Identify the prepared drink | `beverage` | The result describes the completed action. |
| Report payment and change | `paidCents`, `changeCents` | These values remain useful after session reset. |
| Distinguish recipe units | enum constants | The key carries the measurement meaning. |

| Caller need or transition | Method | Result or mutation |
|---|---|---|
| Receive purchase outcome | record accessors | Exposes immutable data with no follow-up mutation. |
| Preserve a completed result | record constructor | Stores the outcome already computed by `dispense()`. |
| Address an ingredient | enum value | Supplies a closed, type-safe map key. |

```text
record DispenseResult
  beverage: Beverage
  paidCents: int
  changeCents: int

enum Ingredient
  WATER_ML
  COFFEE_GRAMS
  MILK_ML
```

**Invariant owner:** `dispense()` computes `changeCents` as `paidCents - beverage.priceCents()` after checking payment. The result records that calculation. Ingredient keys state their unit.

**Knowledge boundary:** These values do not coordinate the purchase or mutate ingredient quantities.

**Collaborators:** `CoffeeVendingMachine` creates the result. `Beverage` and `IngredientInventory` share the ingredient keys.

## Final Class Design

```mermaid
classDiagram
    class CoffeeVendingMachine {
      -menuByCode: Map
      -selected: Beverage
      -balanceCents: int
      +select(code)
      +insertCoin(cents)
      +dispense() DispenseResult
      +cancel() int
    }
    class IngredientInventory {
      -quantities: Map
      +canPrepare(recipe) boolean
      +consume(recipe)
      +quantityOf(ingredient) int
    }
    class Beverage {
      +code: String
      +name: String
      +priceCents: int
      +recipe: Map
    }
    class DispenseResult {
      +beverage: Beverage
      +paidCents: int
      +changeCents: int
    }
    class Ingredient {
      WATER_ML
      COFFEE_GRAMS
      MILK_ML
    }
    CoffeeVendingMachine *-- Beverage : owns menu
    CoffeeVendingMachine *-- IngredientInventory : owns workflow access
    CoffeeVendingMachine --> DispenseResult : returns
    Beverage --> Ingredient : recipe keys
    IngredientInventory --> Ingredient : quantity keys
    DispenseResult --> Beverage : prepared drink
```

The machine owns the customer session. The inventory owns all mutable ingredient stock. `Beverage` connects them through an immutable recipe, so payment logic never performs ingredient-specific decrements.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Selected : select available beverage
    Selected --> Selected : insert supported coin
    Selected --> Idle : cancel and refund
    Selected --> Idle : dispense and return change
```

The lifecycle is intentionally small. Payment readiness is calculated from the selected price and current balance rather than stored as another state.

## Core Implementation

Start with `select`, `IngredientInventory.consume`, and `dispense`, since they establish lookup, stock ownership, and purchase completion. Then add `insertCoin`, `cancel`, the small data types, and the demo. All of this belongs to the interview implementation.

### Operation: select an available beverage

`select(code)` first protects the one-session rule. It then resolves the code and asks the inventory whether the fixed recipe is available. `selected` changes only after all checks pass.

```text
if a selected beverage already exists: reject
beverage = menuByCode[code]
if beverage is missing: reject
if inventory cannot prepare beverage.recipe: reject
selected = beverage
```

An unavailable latte does not create a half-started session. The customer may immediately select another menu item.

The null check belongs immediately after `menuByCode.get(code)`: that lookup can fail for a caller's choice. Once a beverage is found, its fields come from the trusted setup.

### Operation: consume a complete recipe

The inventory performs two loops. The first loop is read-only and rejects an unavailable recipe. The second loop executes only after every requirement is known to fit.

```text
for each (ingredient, required) in recipe:
    if quantityOf(ingredient) < required: reject

for each (ingredient, required) in recipe:
    quantity[ingredient] = quantityOf(ingredient) - required
```

This mutation order is the main correctness proof. With water 40, coffee 18, and milk 100, a latte requiring 120 ml of milk fails during the first loop. Water and coffee remain untouched.

### Operation: dispense the selected drink

`dispense()` checks selection and payment, then asks the inventory to consume the recipe. On success, it records the result and clears both session fields.

```text
if selected is missing: reject
if balance < selected.price: reject

inventory.consume(selected.recipe)
result = DispenseResult(selected, balance, balance - selected.price)
clear selected beverage and balance
return result
```

`select()` gives early feedback about an unavailable drink. `consume()` owns the check that protects its stock mutation. `dispense()` delegates to it directly, without another availability check of its own. If consumption fails, the result and session reset are never reached, so the customer can still cancel for a refund.

`insertCoin()` checks that a drink is selected and the denomination is supported, then adds the amount. `cancel()` saves the current balance, clears the session, and returns the saved amount. Built-in exceptions are sufficient for the rejected operations.

## Complete Runnable Implementation

The solution uses standard Java packages without a framework:

```text
solution/
└── src/
    ├── main/java/coffeevendingmachine/
    │   ├── model/
    │   │   ├── Beverage.java
    │   │   ├── DispenseResult.java
    │   │   ├── Ingredient.java
    │   │   └── IngredientInventory.java
    │   ├── service/
    │   │   └── CoffeeVendingMachine.java
    │   └── demo/
    │       └── Main.java
    └── test/java/coffeevendingmachine/
        └── SolutionTest.java
```

The `model` package owns domain values and ingredient state. `service` contains the public purchase workflow. `demo` and the test root depend on that API; the model never depends on the service.

### What you would type in the round

The six application files under `src/main/java`, including the demo, contain 170 lines with imports and blank lines included. Of those, 136 lines define the model and workflow; 34 lines configure two drinks and run one purchase. This is the complete application reproduced in the appendix.

A possible 60-minute plan is 5 minutes for scope, 10 for class design, 30 to type the application and demo, 5 to verify, and 10 for questions or corrections. Typing speed varies; the budget is a planning estimate. The code has four customer operations and two stock loops, with routine records filling in the data model.

`SolutionTest.java` is additional study support. During the round, run the short demo and trace a failed purchase. The test file automates those checks so you can change the implementation while practicing.

Source files:

- [`CoffeeVendingMachine.java`](solution/src/main/java/coffeevendingmachine/service/CoffeeVendingMachine.java)
- [`IngredientInventory.java`](solution/src/main/java/coffeevendingmachine/model/IngredientInventory.java)
- [`Beverage.java`](solution/src/main/java/coffeevendingmachine/model/Beverage.java)
- [`DispenseResult.java`](solution/src/main/java/coffeevendingmachine/model/DispenseResult.java)
- [`Ingredient.java`](solution/src/main/java/coffeevendingmachine/model/Ingredient.java)
- [`Main.java`](solution/src/main/java/coffeevendingmachine/demo/Main.java)
- [`SolutionTest.java`](solution/src/test/java/coffeevendingmachine/SolutionTest.java)

Run from `solution/`:

```bash
mkdir -p out
javac -d out $(find src/main/java src/test/java -name '*.java' | sort)
java -ea -cp out coffeevendingmachine.SolutionTest
java -cp out coffeevendingmachine.demo.Main
```

Verified with `javac 25.0.4.1`:

```text
All coffee vending machine checks passed.
Dispensed Latte; change: 50 cents; milk remaining: 380 ml
```

The matching PDF contains this same article followed by every source and test file in **Appendix: Complete Runnable Code**.

## Verification Walkthrough

Start with a latte priced at 250 cents. Its recipe needs 40 ml water, 18 g coffee, and 120 ml milk. Inventory starts with 500 ml water, 100 g coffee, and 500 ml milk.

1. `select("LAT")` resolves the latte and asks `IngredientInventory.canPrepare(recipe)`. All quantities fit, so the machine stores the beverage. Inventory has not changed.
2. `insertCoin(200)` and `insertCoin(100)` move the session balance to 300 cents.
3. `dispense()` confirms that the 300-cent balance covers the 250-cent price and calls `IngredientInventory.consume(recipe)`.
4. `IngredientInventory.consume(recipe)` completes its validation pass, then decrements all three quantities. Water becomes 460, coffee becomes 82, and milk becomes 380.
5. The machine creates the latte result with 50 cents change, clears the selected beverage and balance, and returns the result.
6. An immediate second `dispense()` is rejected because no selection exists. Ingredient quantities remain at the values from the one successful drink.

For the rejection trace, try dispensing after inserting only 200 cents. The payment check fails before any stock mutation; adding another coin can complete the same purchase, or cancelling can refund it. Separately, a recipe that lacks milk must leave the available water and coffee untouched.

The study checks exercise caller errors, a successful retry with change, cancellation and session reset, and all-or-nothing stock consumption. They use valid setup data throughout.

## Extensibility

### Track physical change coins

Add a `ChangeInventory` that can both calculate and reserve a denomination combination. `dispense()` must verify drink ingredients and change availability before either resource changes. That creates a larger atomic operation and belongs beyond the junior base.

### Add drink customizations

Represent a customer order separately from the configured `Beverage`. The order can derive an adjusted recipe and price for an extra shot or different size. The existing inventory API can still consume the resulting recipe map.

### Model real brewing progress

Introduce states such as `HEATING`, `GRINDING`, `BREWING`, `DISPENSING`, and `FAILED` only when hardware reports asynchronous events. A controller would then advance legal transitions and decide how to refund after failure.

### Support restocking

Add `restock(ingredient, amount)` to `IngredientInventory` and reject non-positive amounts at that new caller boundary. If administrators can edit recipes or prices too, validate those fields when accepting the edit. This changes the input contract; the base demo still uses fixed configuration.

## What Is Expected at Each Level

### Junior

A strong junior solution should identify the machine, beverage, and ingredient inventory; use integer money; keep quantities non-negative; validate the full recipe before decrementing anything; and demonstrate both a successful purchase and rejected operations. A map-based recipe and four public machine operations are enough. Strategy, State, Factory, and hardware classes are unnecessary for this contract.

An interviewer may hint that ingredient consumption needs two passes or that money should use integer cents. After that hint, the candidate should be able to finish the application and a short demonstration. More detailed automated tests can be useful during practice.

### Mid-level

A mid-level candidate should reach the all-or-nothing recipe invariant without prompting, defend the source of truth for inventory, explain the trusted-setup boundary, and describe how change inventory would expand the transaction boundary.

### Senior

A senior candidate should clarify concurrent sessions and physical failure semantics early. They should describe how to reserve ingredients and change atomically, how an asynchronous brewer reports completion, and which guarantees remain local versus distributed. Those concerns should stay out of the junior implementation unless the interviewer changes the contract.
