package stackoverflow.domain;

public enum Vote {
    UP(1), DOWN(-1), NONE(0);

    final int value;

    Vote(int value) {
        this.value = value;
    }
}
