package coffeevendingmachine;

import coffeevendingmachine.model.Beverage;
import coffeevendingmachine.model.DispenseResult;
import coffeevendingmachine.model.Ingredient;
import coffeevendingmachine.model.IngredientInventory;
import coffeevendingmachine.service.CoffeeVendingMachine;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

public final class SolutionTest {
    public static void main(String[] args) {
        Beverage latte = new Beverage("LAT", "Latte", 250, Map.of(
                Ingredient.WATER_ML, 40, Ingredient.COFFEE_GRAMS, 18,
                Ingredient.MILK_ML, 120));
        IngredientInventory inventory = new IngredientInventory(Map.of(
                Ingredient.WATER_ML, 500, Ingredient.COFFEE_GRAMS, 100,
                Ingredient.MILK_ML, 500));
        CoffeeVendingMachine machine = new CoffeeVendingMachine(List.of(latte), inventory);

        // Caller errors must leave the purchase usable.
        expectRejected(() -> machine.select("UNKNOWN"));
        expectRejected(() -> machine.insertCoin(100));
        machine.select("LAT");
        expectRejected(() -> machine.select("LAT"));
        expectRejected(() -> machine.insertCoin(30));
        machine.insertCoin(200);
        expectRejected(machine::dispense);
        assert inventory.quantityOf(Ingredient.WATER_ML) == 500;
        assert inventory.quantityOf(Ingredient.COFFEE_GRAMS) == 100;
        assert inventory.quantityOf(Ingredient.MILK_ML) == 500;

        // The same session succeeds after adding enough money.
        machine.insertCoin(100);
        DispenseResult result = machine.dispense();
        assert result.beverage().equals(latte);
        assert result.paidCents() == 300;
        assert result.changeCents() == 50;
        assert inventory.quantityOf(Ingredient.WATER_ML) == 460;
        assert inventory.quantityOf(Ingredient.COFFEE_GRAMS) == 82;
        assert inventory.quantityOf(Ingredient.MILK_ML) == 380;
        expectRejected(machine::dispense);

        // Cancellation refunds only the current session and consumes nothing.
        machine.select("LAT");
        machine.insertCoin(100);
        assert machine.cancel() == 100;
        assert machine.cancel() == 0;
        assert inventory.quantityOf(Ingredient.WATER_ML) == 460;
        assert inventory.quantityOf(Ingredient.COFFEE_GRAMS) == 82;
        assert inventory.quantityOf(Ingredient.MILK_ML) == 380;
        machine.select("LAT");

        // Missing milk must not consume the water or coffee checked before it.
        Map<Ingredient, Integer> orderedRecipe = new EnumMap<>(Ingredient.class);
        orderedRecipe.putAll(latte.recipe());
        IngredientInventory shortStock = new IngredientInventory(Map.of(
                Ingredient.WATER_ML, 40, Ingredient.COFFEE_GRAMS, 18));
        expectRejected(() -> shortStock.consume(orderedRecipe));
        assert shortStock.quantityOf(Ingredient.WATER_ML) == 40;
        assert shortStock.quantityOf(Ingredient.COFFEE_GRAMS) == 18;
        assert shortStock.quantityOf(Ingredient.MILK_ML) == 0;
        CoffeeVendingMachine emptyMachine = new CoffeeVendingMachine(List.of(latte), shortStock);
        expectRejected(() -> emptyMachine.select("LAT"));

        System.out.println("All coffee vending machine checks passed.");
    }

    private static void expectRejected(Runnable action) {
        try {
            action.run();
        } catch (IllegalArgumentException | IllegalStateException expected) {
            return;
        }
        throw new AssertionError("Expected the operation to be rejected");
    }
}
