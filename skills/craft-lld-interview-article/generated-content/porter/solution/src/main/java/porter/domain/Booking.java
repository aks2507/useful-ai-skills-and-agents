package porter.domain;

public final class Booking {
    public final int id;
    public final int customerId;
    public final Driver driver;
    public final String pickup;
    public final String drop;
    public final int fareRupees;
    private BookingStatus status = BookingStatus.ASSIGNED;

    Booking(int id, int customerId, Driver driver, String pickup,
            String drop, int fareRupees) {
        this.id = id;
        this.customerId = customerId;
        this.driver = driver;
        this.pickup = pickup;
        this.drop = drop;
        this.fareRupees = fareRupees;
    }

    public BookingStatus status() {
        return status;
    }

    void pickUp() {
        moveFrom(BookingStatus.ASSIGNED, BookingStatus.IN_TRANSIT);
    }

    void deliver() {
        moveFrom(BookingStatus.IN_TRANSIT, BookingStatus.DELIVERED);
    }

    void cancel(int customerId) {
        if (customerId != this.customerId) {
            throw new IllegalArgumentException("Only the booking customer can cancel");
        }
        moveFrom(BookingStatus.ASSIGNED, BookingStatus.CANCELLED);
    }

    private void moveFrom(BookingStatus expected, BookingStatus next) {
        if (status != expected) {
            throw new IllegalStateException("Cannot change " + status + " to " + next);
        }
        status = next;
    }
}
