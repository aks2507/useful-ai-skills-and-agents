package stackoverflow.domain;

import java.util.HashMap;
import java.util.Map;

public abstract class Post {
    public final int id;
    public final int authorId;
    public final String body;
    private final Map<Integer, Vote> votes = new HashMap<>();

    Post(int id, int authorId, String body) {
        if (body == null || body.isBlank()) {
            throw new IllegalArgumentException("Post body must not be blank");
        }
        this.id = id;
        this.authorId = authorId;
        this.body = body;
    }

    void vote(int userId, Vote vote) {
        if (userId == authorId) {
            throw new IllegalArgumentException("Cannot vote on your own post");
        }
        if (vote == Vote.NONE) {
            votes.remove(userId);
        } else {
            votes.put(userId, vote);
        }
    }

    public int score() {
        int total = 0;
        for (Vote vote : votes.values()) {
            total += vote.value;
        }
        return total;
    }
}
