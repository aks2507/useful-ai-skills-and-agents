package coffeevendingmachine.model;

public record DispenseResult(
        Beverage beverage,
        int paidCents,
        int changeCents) {

    public DispenseResult {
        if (beverage == null) {
            throw new IllegalArgumentException("Beverage is required");
        }
        if (paidCents < beverage.priceCents()) {
            throw new IllegalArgumentException("Payment cannot be below the beverage price");
        }
        if (changeCents != paidCents - beverage.priceCents()) {
            throw new IllegalArgumentException("Change must equal payment minus price");
        }
    }
}
