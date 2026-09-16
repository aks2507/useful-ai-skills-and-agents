package stackoverflow.demo;

import stackoverflow.domain.Answer;
import stackoverflow.domain.Forum;
import stackoverflow.domain.Question;
import stackoverflow.domain.Vote;

public final class Main {
    public static void main(String[] args) {
        Forum forum = new Forum();
        Question question = forum.askQuestion(10, "Why is my task running twice?",
                "A retry submits the same task again. How can I prevent duplicate work?");
        Answer first = forum.answerQuestion(20, question.id, "Track a stable task ID.");
        Answer second = forum.answerQuestion(30, question.id, "Record completed task IDs.");
        forum.vote(40, question.id, Vote.UP);
        forum.vote(40, first.id, Vote.UP);
        forum.vote(40, first.id, Vote.UP);
        forum.vote(40, first.id, Vote.DOWN);
        forum.acceptAnswer(10, question.id, first.id);
        forum.acceptAnswer(10, question.id, second.id);
        System.out.println("Question #" + question.id + " score=" + question.score());
        for (Answer answer : forum.question(question.id).answers()) {
            System.out.println("Answer #" + answer.id + " score=" + answer.score());
        }
        System.out.println("Accepted answer: #" + question.acceptedAnswer().id);
    }
}
