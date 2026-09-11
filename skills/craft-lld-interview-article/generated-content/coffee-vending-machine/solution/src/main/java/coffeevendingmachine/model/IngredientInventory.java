package coffeevendingmachine.model;

import java.util.EnumMap;
import java.util.Map;

public final class IngredientInventory {
    private final Map<Ingredient, Integer> quantities = new EnumMap<>(Ingredient.class);

    public IngredientInventory(Map<Ingredient, Integer> initialQuantities) {
        quantities.putAll(initialQuantities);
    }

    public boolean canPrepare(Map<Ingredient, Integer> recipe) {
        for (var entry : recipe.entrySet()) {
            if (quantityOf(entry.getKey()) < entry.getValue()) {
                return false;
            }
        }
        return true;
    }

    public void consume(Map<Ingredient, Integer> recipe) {
        if (!canPrepare(recipe)) {
            throw new IllegalStateException("Not enough ingredients for this beverage");
        }

        for (var entry : recipe.entrySet()) {
            Ingredient ingredient = entry.getKey();
            quantities.put(ingredient, quantityOf(ingredient) - entry.getValue());
        }
    }

    public int quantityOf(Ingredient ingredient) {
        return quantities.getOrDefault(ingredient, 0);
    }
}
