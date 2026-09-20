package porter.demo;

import java.util.List;
import porter.domain.Booking;
import porter.domain.DeliveryService;
import porter.domain.Driver;
import porter.domain.VehicleType;

public final class Main {
    public static void main(String[] args) {
        DeliveryService service = new DeliveryService(List.of(
                new Driver(7, VehicleType.TWO_WHEELER),
                new Driver(9, VehicleType.MINI_TRUCK)));
        Booking first = service.book(10, "Indiranagar", "Koramangala",
                VehicleType.MINI_TRUCK, 5);
        System.out.println("Booking #" + first.id + ": driver=" + first.driver.id
                + ", fare=INR " + first.fareRupees + ", " + first.status()
                + ", available=" + first.driver.isAvailable());
        try {
            service.book(20, "Shop B", "Warehouse B", VehicleType.MINI_TRUCK, 4);
        } catch (IllegalStateException e) {
            System.out.println("Second truck request: " + e.getMessage());
        }
        service.pickUp(first.id);
        service.deliver(first.id);
        System.out.println("Booking #" + first.id + ": " + first.status()
                + ", available=" + first.driver.isAvailable());
        Booking second = service.book(20, "Shop B", "Warehouse B",
                VehicleType.MINI_TRUCK, 4);
        System.out.println("Booking #" + second.id + ": driver=" + second.driver.id
                + ", fare=INR " + second.fareRupees + ", " + second.status()
                + ", available=" + second.driver.isAvailable());
    }
}
