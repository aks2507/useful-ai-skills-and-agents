package coffeevendingmachine.demo;

import coffeevendingmachine.model.Beverage;
import coffeevendingmachine.model.DispenseResult;
import coffeevendingmachine.model.Ingredient;
import coffeevendingmachine.model.IngredientInventory;
import coffeevendingmachine.service.CoffeeVendingMachine;
import java.util.List;
import java.util.Map;

public final class Main {
    public static void main(String[] args) {
        Beverage espresso = new Beverage("ESP", "Espresso", 150, Map.of(
                Ingredient.WATER_ML, 50, Ingredient.COFFEE_GRAMS, 18));
        Beverage latte = new Beverage("LAT", "Latte", 250, Map.of(
                Ingredient.WATER_ML, 40, Ingredient.COFFEE_GRAMS, 18,
                Ingredient.MILK_ML, 120));
        IngredientInventory inventory = new IngredientInventory(Map.of(
                Ingredient.WATER_ML, 500,
                Ingredient.COFFEE_GRAMS, 100,
                Ingredient.MILK_ML, 500));
        CoffeeVendingMachine machine = new CoffeeVendingMachine(
                List.of(espresso, latte), inventory);

        machine.select("LAT");
        machine.insertCoin(200);
        machine.insertCoin(100);
        DispenseResult result = machine.dispense();

        System.out.printf("Dispensed %s; change: %d cents; milk remaining: %d ml%n",
                result.beverage().name(), result.changeCents(),
                inventory.quantityOf(Ingredient.MILK_ML));
    }
}
