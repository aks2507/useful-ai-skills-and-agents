package porter.domain;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class DeliveryService {
    private final List<Driver> drivers;
    private final Map<Integer, Booking> bookings = new HashMap<>();
    private int nextId = 1;

    public DeliveryService(List<Driver> drivers) {
        this.drivers = List.copyOf(drivers);
    }

    public Booking book(int customerId, String pickup, String drop,
                        VehicleType type, int distanceKm) {
        if (type == null || distanceKm <= 0) {
            throw new IllegalArgumentException("Choose a vehicle and a positive distance");
        }
        for (Driver driver : drivers) {
            if (driver.vehicleType == type && driver.isAvailable()) {
                Booking booking = new Booking(nextId, customerId, driver,
                        pickup, drop, type.fareFor(distanceKm));
                driver.assign();
                bookings.put(nextId++, booking);
                return booking;
            }
        }
        throw new IllegalStateException("No available driver");
    }

    public void pickUp(int bookingId) {
        booking(bookingId).pickUp();
    }

    public void deliver(int bookingId) {
        Booking booking = booking(bookingId);
        booking.deliver();
        booking.driver.release();
    }

    public void cancel(int customerId, int bookingId) {
        Booking booking = booking(bookingId);
        booking.cancel(customerId);
        booking.driver.release();
    }

    public Booking booking(int bookingId) {
        Booking booking = bookings.get(bookingId);
        if (booking == null) {
            throw new IllegalArgumentException("Unknown booking ID: " + bookingId);
        }
        return booking;
    }
}
