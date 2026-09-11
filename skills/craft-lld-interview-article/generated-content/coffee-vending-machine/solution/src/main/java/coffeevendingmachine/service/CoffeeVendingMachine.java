package coffeevendingmachine.service;

import coffeevendingmachine.model.Beverage;
import coffeevendingmachine.model.DispenseResult;
import coffeevendingmachine.model.IngredientInventory;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public final class CoffeeVendingMachine {
    private static final Set<Integer> SUPPORTED_COINS = Set.of(25, 50, 100, 200);

    private final Map<String, Beverage> menuByCode = new HashMap<>();
    private final IngredientInventory inventory;
    private Beverage selected;
    private int balanceCents;

    public CoffeeVendingMachine(
            Collection<Beverage> menu,
            IngredientInventory inventory) {
        for (Beverage beverage : menu) {
            menuByCode.put(beverage.code(), beverage);
        }
        this.inventory = inventory;
    }

    public void select(String code) {
        if (selected != null) {
            throw new IllegalStateException("Cancel or dispense the current selection first");
        }

        Beverage beverage = menuByCode.get(code);
        if (beverage == null) {
            throw new IllegalArgumentException("Unknown beverage code: " + code);
        }
        if (!inventory.canPrepare(beverage.recipe())) {
            throw new IllegalStateException("Beverage is unavailable: " + code);
        }
        selected = beverage;
    }

    public void insertCoin(int cents) {
        if (selected == null) {
            throw new IllegalStateException("Select a beverage first");
        }
        if (!SUPPORTED_COINS.contains(cents)) {
            throw new IllegalArgumentException("Unsupported coin: " + cents);
        }
        balanceCents += cents;
    }

    public DispenseResult dispense() {
        if (selected == null) {
            throw new IllegalStateException("Select a beverage first");
        }
        if (balanceCents < selected.priceCents()) {
            throw new IllegalStateException("Insufficient payment");
        }

        inventory.consume(selected.recipe());
        DispenseResult result = new DispenseResult(
                selected, balanceCents, balanceCents - selected.priceCents());
        clearSession();
        return result;
    }

    public int cancel() {
        int refund = balanceCents;
        clearSession();
        return refund;
    }

    private void clearSession() {
        selected = null;
        balanceCents = 0;
    }
}
