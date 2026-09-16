package stackoverflow.domain;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class Question extends Post {
    public final String title;
    private final Map<Integer, Answer> answers = new LinkedHashMap<>();
    private Answer acceptedAnswer;

    Question(int id, int authorId, String title, String body) {
        super(id, authorId, body);
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("Question title must not be blank");
        }
        this.title = title;
    }

    Answer addAnswer(int answerId, int authorId, String body) {
        Answer answer = new Answer(answerId, authorId, body, id);
        answers.put(answerId, answer);
        return answer;
    }

    void acceptAnswer(int userId, int answerId) {
        if (userId != authorId) {
            throw new IllegalArgumentException("Only the question author can accept");
        }
        Answer answer = answers.get(answerId);
        if (answer == null) {
            throw new IllegalArgumentException("Answer does not belong to this question");
        }
        acceptedAnswer = answer;
    }

    public List<Answer> answers() {
        return List.copyOf(answers.values());
    }

    public Answer acceptedAnswer() {
        return acceptedAnswer;
    }
}
