package porter.domain;

public enum VehicleType {
    TWO_WHEELER(30, 8), MINI_TRUCK(150, 20);

    private final int baseRupees;
    private final int rupeesPerKm;

    VehicleType(int baseRupees, int rupeesPerKm) {
        this.baseRupees = baseRupees;
        this.rupeesPerKm = rupeesPerKm;
    }

    public int fareFor(int distanceKm) {
        return baseRupees + rupeesPerKm * distanceKm;
    }
}
