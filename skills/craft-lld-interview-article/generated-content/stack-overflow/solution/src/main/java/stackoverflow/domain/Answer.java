package stackoverflow.domain;

public final class Answer extends Post {
    public final int questionId;

    Answer(int id, int authorId, String body, int questionId) {
        super(id, authorId, body);
        this.questionId = questionId;
    }
}
