package porter.domain;

public final class Driver {
    public final int id;
    public final VehicleType vehicleType;
    private boolean available = true;

    public Driver(int id, VehicleType vehicleType) {
        this.id = id;
        this.vehicleType = vehicleType;
    }

    public boolean isAvailable() {
        return available;
    }

    void assign() {
        available = false;
    }

    void release() {
        available = true;
    }
}
