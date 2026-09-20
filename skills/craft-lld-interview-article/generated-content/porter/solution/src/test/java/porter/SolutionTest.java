package porter;

import java.util.List;
import porter.domain.Booking;
import porter.domain.BookingStatus;
import porter.domain.DeliveryService;
import porter.domain.Driver;
import porter.domain.VehicleType;

public final class SolutionTest {
    public static void main(String[] args) {
        matchingAndFares();
        lifecycleAndReuse();
        cancellationAndStaleRequests();
        invalidBookingDoesNotAllocate();
        unknownBookingDoesNotMutate();
        retainedHistoryAndReuse();
        System.out.println("6 focused tests passed");
    }

    private static DeliveryService service() {
        return new DeliveryService(List.of(new Driver(7, VehicleType.TWO_WHEELER),
                new Driver(9, VehicleType.MINI_TRUCK)));
    }

    private static Booking truck(DeliveryService service, int customerId) {
        return service.book(customerId, "Shop", "Warehouse", VehicleType.MINI_TRUCK, 5);
    }

    private static void matchingAndFares() {
        Driver bikeDriver = new Driver(7, VehicleType.TWO_WHEELER);
        Driver firstTruckDriver = new Driver(9, VehicleType.MINI_TRUCK);
        Driver secondTruckDriver = new Driver(11, VehicleType.MINI_TRUCK);
        DeliveryService service = new DeliveryService(List.of(
                bikeDriver, firstTruckDriver, secondTruckDriver));
        assert bikeDriver.isAvailable() && firstTruckDriver.isAvailable();
        Booking first = truck(service, 10);
        Booking second = truck(service, 20);
        assert first.driver.id == 9 && second.driver.id == 11;
        assert !firstTruckDriver.isAvailable() && !secondTruckDriver.isAvailable();
        assert first.fareRupees == 250 && first.pickup.equals("Shop");
        rejects(IllegalStateException.class, () -> truck(service, 30));
        assert bikeDriver.isAvailable() && !firstTruckDriver.isAvailable();
        Booking bike = service.book(30, "A", "B", VehicleType.TWO_WHEELER, 5);
        assert bike.id == 3 && bike.driver.id == 7 && bike.fareRupees == 70;
        assert !bikeDriver.isAvailable();
        assert service.booking(first.id) == first;
    }

    private static void lifecycleAndReuse() {
        DeliveryService service = service();
        Booking first = truck(service, 10);
        rejects(IllegalStateException.class, () -> service.deliver(first.id));
        assert first.status() == BookingStatus.ASSIGNED && !first.driver.isAvailable();
        service.pickUp(first.id);
        rejects(IllegalStateException.class, () -> service.pickUp(first.id));
        rejects(IllegalStateException.class, () -> service.cancel(10, first.id));
        rejects(IllegalStateException.class, () -> truck(service, 20));
        assert first.status() == BookingStatus.IN_TRANSIT && !first.driver.isAvailable();
        service.deliver(first.id);
        assert first.driver.isAvailable();
        Booking second = truck(service, 20);
        rejects(IllegalStateException.class, () -> service.deliver(first.id));
        rejects(IllegalStateException.class, () -> service.cancel(10, first.id));
        rejects(IllegalStateException.class, () -> service.pickUp(first.id));
        rejects(IllegalStateException.class, () -> truck(service, 30));
        assert first.status() == BookingStatus.DELIVERED;
        assert second.id == 2 && second.driver == first.driver;
        assert second.status() == BookingStatus.ASSIGNED && !second.driver.isAvailable();
    }

    private static void cancellationAndStaleRequests() {
        DeliveryService service = service();
        Booking first = truck(service, 10);
        rejects(IllegalArgumentException.class, () -> service.cancel(20, first.id));
        assert first.status() == BookingStatus.ASSIGNED && !first.driver.isAvailable();
        service.cancel(10, first.id);
        assert first.driver.isAvailable();
        rejects(IllegalStateException.class, () -> service.cancel(10, first.id));
        assert first.driver.isAvailable();
        Booking second = truck(service, 20);
        rejects(IllegalStateException.class, () -> service.cancel(10, first.id));
        rejects(IllegalStateException.class, () -> service.pickUp(first.id));
        rejects(IllegalStateException.class, () -> service.deliver(first.id));
        rejects(IllegalStateException.class, () -> truck(service, 30));
        assert first.status() == BookingStatus.CANCELLED;
        assert second.status() == BookingStatus.ASSIGNED && !second.driver.isAvailable();
        assert first.driver == second.driver;
    }

    private static void invalidBookingDoesNotAllocate() {
        Driver driver = new Driver(9, VehicleType.MINI_TRUCK);
        DeliveryService service = new DeliveryService(List.of(driver));
        rejects(IllegalArgumentException.class,
                () -> service.book(10, "A", "B", null, 5));
        rejects(IllegalArgumentException.class,
                () -> service.book(10, "A", "B", VehicleType.MINI_TRUCK, 0));
        assert driver.isAvailable();
        assert truck(service, 10).id == 1;
        assert !driver.isAvailable();
    }

    private static void unknownBookingDoesNotMutate() {
        DeliveryService service = service();
        Booking booking = truck(service, 10);
        rejects(IllegalArgumentException.class, () -> service.booking(999));
        rejects(IllegalArgumentException.class, () -> service.cancel(10, 999));
        rejects(IllegalArgumentException.class, () -> service.deliver(999));
        rejects(IllegalArgumentException.class, () -> service.pickUp(999));
        assert booking.status() == BookingStatus.ASSIGNED && !booking.driver.isAvailable();
        rejects(IllegalStateException.class, () -> truck(service, 20));
    }

    private static void retainedHistoryAndReuse() {
        DeliveryService service = service();
        for (int i = 0; i < 1000; i++) {
            Booking booking = truck(service, 10);
            service.pickUp(booking.id);
            service.deliver(booking.id);
            assert booking.driver.isAvailable();
        }
        Booking current = truck(service, 20);
        assert current.id == 1001 && !current.driver.isAvailable();
        assert service.booking(1).status() == BookingStatus.DELIVERED;
        assert service.booking(1).driver == current.driver;
    }

    private static void rejects(Class<? extends RuntimeException> type, Runnable action) {
        try {
            action.run();
            throw new AssertionError("Expected " + type.getSimpleName());
        } catch (RuntimeException e) {
            if (!type.isInstance(e)) {
                throw new AssertionError("Wrong exception", e);
            }
        }
    }
}
