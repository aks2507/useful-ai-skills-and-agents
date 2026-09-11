package coffeevendingmachine.model;

import java.util.EnumMap;
import java.util.Map;

public record Beverage(
        String code,
        String name,
        int priceCents,
        Map<Ingredient, Integer> recipe) {

    public Beverage {
        if (code == null || code.isBlank()) {
            throw new IllegalArgumentException("Beverage code must not be blank");
        }
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Beverage name must not be blank");
        }
        if (priceCents <= 0) {
            throw new IllegalArgumentException("Price must be positive");
        }
        if (recipe == null || recipe.isEmpty()) {
            throw new IllegalArgumentException("Recipe must contain at least one ingredient");
        }

        EnumMap<Ingredient, Integer> copy = new EnumMap<>(Ingredient.class);
        for (Map.Entry<Ingredient, Integer> entry : recipe.entrySet()) {
            Ingredient ingredient = entry.getKey();
            Integer amount = entry.getValue();
            if (ingredient == null || amount == null || amount <= 0) {
                throw new IllegalArgumentException("Recipe amounts must be positive");
            }
            copy.put(ingredient, amount);
        }
        recipe = Map.copyOf(copy);
    }
}
