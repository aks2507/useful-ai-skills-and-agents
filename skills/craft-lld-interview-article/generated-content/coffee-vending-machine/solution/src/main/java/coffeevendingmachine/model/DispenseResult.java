package coffeevendingmachine.model;

public record DispenseResult(
        Beverage beverage,
        int paidCents,
        int changeCents) {}
