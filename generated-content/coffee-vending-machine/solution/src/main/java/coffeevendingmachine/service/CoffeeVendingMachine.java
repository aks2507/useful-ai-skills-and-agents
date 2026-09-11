package coffeevendingmachine.service;

import coffeevendingmachine.model.Beverage;
import coffeevendingmachine.model.DispenseResult;
import coffeevendingmachine.model.IngredientInventory;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

public final class CoffeeVendingMachine {
    private static final Set<Integer> SUPPORTED_COINS = Set.of(25, 50, 100, 200);

    private final Map<String, Beverage> menuByCode;
    private final IngredientInventory inventory;
    private String selectedCode;
    private int balanceCents;

    public CoffeeVendingMachine(
            Collection<Beverage> menu,
            IngredientInventory inventory) {
        if (menu == null || menu.isEmpty()) {
            throw new IllegalArgumentException("Menu must not be empty");
        }
        if (inventory == null) {
            throw new IllegalArgumentException("Ingredient inventory is required");
        }

        this.menuByCode = new LinkedHashMap<>();
        for (Beverage beverage : menu) {
            if (beverage == null) {
                throw new IllegalArgumentException("Menu beverage must not be null");
            }
            if (menuByCode.putIfAbsent(beverage.code(), beverage) != null) {
                throw new IllegalArgumentException(
                        "Duplicate beverage code: " + beverage.code());
            }
        }
        this.inventory = inventory;
    }

    public void select(String code) {
        if (selectedCode != null) {
            throw new IllegalStateException("Cancel or dispense the current selection first");
        }

        Beverage beverage = menuByCode.get(code);
        if (beverage == null) {
            throw new IllegalArgumentException("Unknown beverage code: " + code);
        }
        if (!inventory.canPrepare(beverage.recipe())) {
            throw new IllegalStateException("Beverage is unavailable: " + code);
        }
        selectedCode = code;
    }

    public void insertCoin(int cents) {
        requireSelection();
        if (!SUPPORTED_COINS.contains(cents)) {
            throw new IllegalArgumentException("Unsupported coin: " + cents);
        }
        balanceCents += cents;
    }

    public DispenseResult dispense() {
        Beverage beverage = requireSelection();
        if (balanceCents < beverage.priceCents()) {
            throw new IllegalStateException("Insufficient payment");
        }
        if (!inventory.canPrepare(beverage.recipe())) {
            throw new IllegalStateException("Beverage is no longer available");
        }

        DispenseResult result = new DispenseResult(
                beverage,
                balanceCents,
                balanceCents - beverage.priceCents());
        inventory.consume(beverage.recipe());
        clearSession();
        return result;
    }

    public int cancel() {
        int refund = balanceCents;
        clearSession();
        return refund;
    }

    private Beverage requireSelection() {
        if (selectedCode == null) {
            throw new IllegalStateException("Select a beverage first");
        }
        return menuByCode.get(selectedCode);
    }

    private void clearSession() {
        selectedCode = null;
        balanceCents = 0;
    }
}
