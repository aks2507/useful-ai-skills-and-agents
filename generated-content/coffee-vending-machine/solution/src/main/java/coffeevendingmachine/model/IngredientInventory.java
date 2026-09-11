package coffeevendingmachine.model;

import java.util.EnumMap;
import java.util.Map;

public final class IngredientInventory {
    private final EnumMap<Ingredient, Integer> quantities;

    public IngredientInventory(Map<Ingredient, Integer> initialQuantities) {
        if (initialQuantities == null) {
            throw new IllegalArgumentException("Initial quantities are required");
        }
        quantities = new EnumMap<>(Ingredient.class);
        for (Ingredient ingredient : Ingredient.values()) {
            int quantity = initialQuantities.getOrDefault(ingredient, 0);
            if (quantity < 0) {
                throw new IllegalArgumentException("Ingredient quantity must not be negative");
            }
            quantities.put(ingredient, quantity);
        }
    }

    public boolean canPrepare(Map<Ingredient, Integer> recipe) {
        validateRecipe(recipe);
        for (Ingredient ingredient : Ingredient.values()) {
            int required = recipe.getOrDefault(ingredient, 0);
            if (quantities.get(ingredient) < required) {
                return false;
            }
        }
        return true;
    }

    public void consume(Map<Ingredient, Integer> recipe) {
        if (!canPrepare(recipe)) {
            throw new IllegalStateException("Not enough ingredients for this beverage");
        }

        for (Ingredient ingredient : Ingredient.values()) {
            int required = recipe.getOrDefault(ingredient, 0);
            quantities.compute(ingredient, (ignored, current) -> current - required);
        }
    }

    public int quantityOf(Ingredient ingredient) {
        if (ingredient == null) {
            throw new IllegalArgumentException("Ingredient is required");
        }
        return quantities.get(ingredient);
    }

    private static void validateRecipe(Map<Ingredient, Integer> recipe) {
        if (recipe == null || recipe.isEmpty()) {
            throw new IllegalArgumentException("Recipe must not be empty");
        }
        for (Map.Entry<Ingredient, Integer> entry : recipe.entrySet()) {
            if (entry.getKey() == null || entry.getValue() == null || entry.getValue() <= 0) {
                throw new IllegalArgumentException("Recipe amounts must be positive");
            }
        }
    }
}
