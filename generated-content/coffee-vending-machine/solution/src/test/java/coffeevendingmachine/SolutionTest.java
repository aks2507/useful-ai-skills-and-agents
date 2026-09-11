package coffeevendingmachine;

import coffeevendingmachine.model.Beverage;
import coffeevendingmachine.model.DispenseResult;
import coffeevendingmachine.model.Ingredient;
import coffeevendingmachine.model.IngredientInventory;
import coffeevendingmachine.service.CoffeeVendingMachine;
import java.util.List;
import java.util.Map;

public final class SolutionTest {
    private SolutionTest() {}

    public static void main(String[] args) {
        successfulLatteConsumesRecipeAndReturnsChange();
        insufficientPaymentPreservesInventoryAndSession();
        unavailableBeverageCannotBeSelected();
        invalidCoinDoesNotIncreaseBalance();
        cancellationReturnsBalanceWithoutConsumingIngredients();
        ingredientConsumptionIsAllOrNothing();
        duplicateMenuCodesAreRejected();
        System.out.println("All coffee vending machine tests passed.");
    }

    private static void successfulLatteConsumesRecipeAndReturnsChange() {
        Fixture fixture = fixture(500, 100, 500);
        fixture.machine.select("LAT");
        fixture.machine.insertCoin(200);
        fixture.machine.insertCoin(100);

        DispenseResult result = fixture.machine.dispense();

        assert result.beverage().equals(fixture.latte);
        assert result.paidCents() == 300;
        assert result.changeCents() == 50;
        assert fixture.inventory.quantityOf(Ingredient.WATER_ML) == 460;
        assert fixture.inventory.quantityOf(Ingredient.COFFEE_GRAMS) == 82;
        assert fixture.inventory.quantityOf(Ingredient.MILK_ML) == 380;
        expectThrows(IllegalStateException.class, fixture.machine::dispense);
    }

    private static void insufficientPaymentPreservesInventoryAndSession() {
        Fixture fixture = fixture(500, 100, 500);
        fixture.machine.select("LAT");
        fixture.machine.insertCoin(200);

        expectThrows(IllegalStateException.class, fixture.machine::dispense);

        assert fixture.inventory.quantityOf(Ingredient.WATER_ML) == 500;
        assert fixture.inventory.quantityOf(Ingredient.COFFEE_GRAMS) == 100;
        assert fixture.inventory.quantityOf(Ingredient.MILK_ML) == 500;
        assert fixture.machine.cancel() == 200;
    }

    private static void unavailableBeverageCannotBeSelected() {
        Fixture fixture = fixture(500, 100, 100);

        expectThrows(IllegalStateException.class, () -> fixture.machine.select("LAT"));
        expectThrows(IllegalStateException.class, () -> fixture.machine.insertCoin(100));
    }

    private static void invalidCoinDoesNotIncreaseBalance() {
        Fixture fixture = fixture(500, 100, 500);
        fixture.machine.select("LAT");

        expectThrows(IllegalArgumentException.class, () -> fixture.machine.insertCoin(30));

        assert fixture.machine.cancel() == 0;
    }

    private static void cancellationReturnsBalanceWithoutConsumingIngredients() {
        Fixture fixture = fixture(500, 100, 500);
        fixture.machine.select("LAT");
        fixture.machine.insertCoin(100);

        assert fixture.machine.cancel() == 100;
        assert fixture.inventory.quantityOf(Ingredient.WATER_ML) == 500;
        assert fixture.inventory.quantityOf(Ingredient.COFFEE_GRAMS) == 100;
        assert fixture.inventory.quantityOf(Ingredient.MILK_ML) == 500;
        fixture.machine.select("LAT");
    }

    private static void ingredientConsumptionIsAllOrNothing() {
        IngredientInventory inventory = new IngredientInventory(Map.of(
                Ingredient.WATER_ML, 100,
                Ingredient.COFFEE_GRAMS, 5,
                Ingredient.MILK_ML, 100));
        Map<Ingredient, Integer> recipe = Map.of(
                Ingredient.WATER_ML, 50,
                Ingredient.COFFEE_GRAMS, 18);

        expectThrows(IllegalStateException.class, () -> inventory.consume(recipe));

        assert inventory.quantityOf(Ingredient.WATER_ML) == 100;
        assert inventory.quantityOf(Ingredient.COFFEE_GRAMS) == 5;
    }

    private static void duplicateMenuCodesAreRejected() {
        Fixture fixture = fixture(500, 100, 500);
        Beverage copy = new Beverage(
                "LAT",
                "Another Latte",
                275,
                fixture.latte.recipe());

        expectThrows(
                IllegalArgumentException.class,
                () -> new CoffeeVendingMachine(
                        List.of(fixture.latte, copy),
                        fixture.inventory));
    }

    private static Fixture fixture(int waterMl, int coffeeGrams, int milkMl) {
        Beverage latte = new Beverage(
                "LAT",
                "Latte",
                250,
                Map.of(
                        Ingredient.WATER_ML, 40,
                        Ingredient.COFFEE_GRAMS, 18,
                        Ingredient.MILK_ML, 120));
        IngredientInventory inventory = new IngredientInventory(Map.of(
                Ingredient.WATER_ML, waterMl,
                Ingredient.COFFEE_GRAMS, coffeeGrams,
                Ingredient.MILK_ML, milkMl));
        return new Fixture(
                latte,
                inventory,
                new CoffeeVendingMachine(List.of(latte), inventory));
    }

    private static void expectThrows(
            Class<? extends RuntimeException> type,
            Runnable operation) {
        try {
            operation.run();
            throw new AssertionError("Expected " + type.getSimpleName());
        } catch (RuntimeException error) {
            if (!type.isInstance(error)) {
                throw error;
            }
        }
    }

    private record Fixture(
            Beverage latte,
            IngredientInventory inventory,
            CoffeeVendingMachine machine) {}
}
