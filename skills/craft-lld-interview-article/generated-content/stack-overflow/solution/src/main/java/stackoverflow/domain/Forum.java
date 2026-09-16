package stackoverflow.domain;

import java.util.HashMap;
import java.util.Map;

public final class Forum {
    private final Map<Integer, Post> posts = new HashMap<>();
    private int nextId = 1;

    public Question askQuestion(int userId, String title, String body) {
        Question question = new Question(nextId, userId, title, body);
        posts.put(nextId++, question);
        return question;
    }

    public Answer answerQuestion(int userId, int questionId, String body) {
        Question question = question(questionId);
        Answer answer = question.addAnswer(nextId, userId, body);
        posts.put(nextId++, answer);
        return answer;
    }

    public void vote(int userId, int postId, Vote vote) {
        if (vote == null) {
            throw new IllegalArgumentException("Choose UP, DOWN, or NONE");
        }
        post(postId).vote(userId, vote);
    }

    public void acceptAnswer(int userId, int questionId, int answerId) {
        question(questionId).acceptAnswer(userId, answerId);
    }

    public Question question(int questionId) {
        Post post = post(questionId);
        if (!(post instanceof Question question)) {
            throw new IllegalArgumentException("Expected a question ID");
        }
        return question;
    }

    private Post post(int postId) {
        Post post = posts.get(postId);
        if (post == null) {
            throw new IllegalArgumentException("Unknown post ID: " + postId);
        }
        return post;
    }
}
