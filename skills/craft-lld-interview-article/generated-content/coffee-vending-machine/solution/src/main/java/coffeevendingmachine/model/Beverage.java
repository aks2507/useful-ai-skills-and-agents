package coffeevendingmachine.model;

import java.util.Map;

public record Beverage(
        String code,
        String name,
        int priceCents,
        Map<Ingredient, Integer> recipe) {}
