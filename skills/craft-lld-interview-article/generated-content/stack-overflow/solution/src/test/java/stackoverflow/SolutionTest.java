package stackoverflow;

import java.util.List;
import stackoverflow.domain.Answer;
import stackoverflow.domain.Forum;
import stackoverflow.domain.Question;
import stackoverflow.domain.Vote;

public final class SolutionTest {
    public static void main(String[] args) {
        postingAndReading();
        voteLifecycle();
        rejectedVotesPreserveScore();
        acceptanceAndReplacement();
        rejectedAcceptancePreservesChoice();
        unknownAndWrongKindIds();
        invalidContentIsNotPublished();
        System.out.println("7 focused tests passed");
    }

    private static void postingAndReading() {
        Forum forum = new Forum();
        Question question = forum.askQuestion(10, "Retries?", "How do I handle retries?");
        Answer answer = forum.answerQuestion(20, question.id, "Use a stable request ID.");
        assert question.id == 1 && answer.id == 2;
        assert question.authorId == 10 && answer.authorId == 20;
        assert question.title.equals("Retries?");
        assert question.body.equals("How do I handle retries?");
        assert answer.body.equals("Use a stable request ID.");
        assert answer.questionId == question.id;
        assert question.acceptedAnswer() == null;
        assert forum.question(question.id) == question;
        List<Answer> earlier = question.answers();
        Answer another = forum.answerQuestion(30, question.id, "Make the operation idempotent.");
        assert earlier.equals(List.of(answer));
        assert question.answers().equals(List.of(answer, another));
    }

    private static void voteLifecycle() {
        Forum forum = new Forum();
        Question question = forum.askQuestion(10, "Retries?", "How do I handle retries?");
        Answer answer = forum.answerQuestion(20, question.id, "Use a stable request ID.");
        for (int postId : List.of(question.id, answer.id)) {
            forum.vote(30, postId, Vote.UP);
            forum.vote(30, postId, Vote.UP);
            assert (postId == question.id ? question : answer).score() == 1;
            forum.vote(30, postId, Vote.DOWN);
            forum.vote(40, postId, Vote.UP);
            assert (postId == question.id ? question : answer).score() == 0;
            forum.vote(30, postId, Vote.NONE);
            forum.vote(30, postId, Vote.NONE);
            assert (postId == question.id ? question : answer).score() == 1;
        }
    }

    private static void rejectedVotesPreserveScore() {
        Forum forum = new Forum();
        Question question = forum.askQuestion(10, "Retries?", "How do I handle retries?");
        Answer answer = forum.answerQuestion(20, question.id, "Use a stable request ID.");
        forum.vote(30, answer.id, Vote.UP);
        rejects(() -> forum.vote(20, answer.id, Vote.DOWN));
        rejects(() -> forum.vote(10, question.id, Vote.UP));
        rejects(() -> forum.vote(30, answer.id, null));
        assert answer.score() == 1 && question.score() == 0;
    }

    private static void acceptanceAndReplacement() {
        Forum forum = new Forum();
        Question question = forum.askQuestion(10, "Retries?", "How do I handle retries?");
        Answer first = forum.answerQuestion(20, question.id, "Use a stable request ID.");
        forum.acceptAnswer(10, question.id, first.id);
        forum.acceptAnswer(10, question.id, first.id);
        assert question.acceptedAnswer() == first;
        Answer own = forum.answerQuestion(10, question.id, "I added deduplication.");
        forum.acceptAnswer(10, question.id, own.id);
        assert question.acceptedAnswer() == own;
        assert question.answers().size() == 2;
        assert first.score() == 0 && own.score() == 0;
    }

    private static void rejectedAcceptancePreservesChoice() {
        Forum forum = new Forum();
        Question question = forum.askQuestion(10, "Retries?", "How do I handle retries?");
        Answer accepted = forum.answerQuestion(20, question.id, "Use a stable request ID.");
        Question other = forum.askQuestion(30, "Timeouts?", "What timeout should I choose?");
        Answer foreign = forum.answerQuestion(40, other.id, "Measure the latency first.");
        forum.acceptAnswer(10, question.id, accepted.id);
        rejects(() -> forum.acceptAnswer(20, question.id, accepted.id));
        rejects(() -> forum.acceptAnswer(10, question.id, foreign.id));
        rejects(() -> forum.acceptAnswer(10, question.id, 999));
        rejects(() -> forum.acceptAnswer(10, question.id, question.id));
        assert question.acceptedAnswer() == accepted;
        assert other.acceptedAnswer() == null;
    }

    private static void unknownAndWrongKindIds() {
        Forum forum = new Forum();
        Question question = forum.askQuestion(10, "Retries?", "How do I handle retries?");
        Answer answer = forum.answerQuestion(20, question.id, "Use a stable request ID.");
        rejects(() -> forum.question(999));
        rejects(() -> forum.question(answer.id));
        rejects(() -> forum.answerQuestion(30, 999, "An answer."));
        rejects(() -> forum.answerQuestion(30, answer.id, "An answer."));
        rejects(() -> forum.vote(30, 999, Vote.UP));
        rejects(() -> forum.acceptAnswer(10, 999, answer.id));
        assert question.answers().equals(List.of(answer));
    }

    private static void invalidContentIsNotPublished() {
        Forum forum = new Forum();
        rejects(() -> forum.askQuestion(10, " ", "Some text."));
        Question question = forum.askQuestion(10, "Retries?", "How do I handle retries?");
        rejects(() -> forum.answerQuestion(20, question.id, null));
        assert question.id == 1 && question.answers().isEmpty();
        Answer answer = forum.answerQuestion(20, question.id, "Use a stable request ID.");
        assert answer.id == 2;
    }

    private static void rejects(Runnable action) {
        try {
            action.run();
            throw new AssertionError("Expected IllegalArgumentException");
        } catch (IllegalArgumentException expected) {
            // The caller mistake must be rejected before changing domain state.
        }
    }
}
