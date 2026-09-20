# Editorial Style and Natural-Prose Audit

## Voice

Write like an experienced interviewer coaching a candidate through a live decision. Be direct, concrete, and candid about what belongs in the round. Prefer a small scenario or state transition before naming a general principle.

Use original wording. Do not reproduce a publisher's distinctive analogies, jokes, prompts, dialogue, or paragraph sequence.

## Cadence

### Give the reader a reason to continue

Open with a small domain action that exposes the central tension. Carry its identifiers and state through the main comparison and verification. The interest should come from seeing a plausible solution meet a revealing case, then watching one small design change fix it. Do not add fictional drama, clickbait, or an unrelated analogy.

Make adjacent paragraphs causally connected: what have we learned, what question is still open, and why is this the next thing to decide? A useful transition names the consequence. A section introduction that only announces the section can usually go.

### Spend explanation where judgment is needed

Prefer one primary explanation of each fact. A table may derive ownership, code may state the operation, and the next paragraph may explain a surprising consequence. They should not all say the same thing. A purposeful replay is valuable when it now proves something new.

Do not narrate a getter, loop, or constructor line by line for an experienced reader. Explain why a field belongs here, why validation precedes this mutation, or what breaks if the order changes. For a junior reader, explain unfamiliar mechanics once before using them; tight prose must not remove prerequisites.

### Make the page readable at two speeds

Headings and selective **bold** should let a scanning reader find the design decisions. The paragraphs between them should still form a continuous argument for someone reading end to end. Bold the decisive rule, changed assumption, or tradeoff at first importance. Use backticks for names and syntax. Avoid entire bold paragraphs, bolding every class mention, and arbitrary emphasis quotas.

Use a figure where the reader would otherwise have to build and compare mental pictures. Write its takeaway caption first, then draw only what supports it. Match the adjacent example and use labels as well as color. See `diagrams.md`. Do not interrupt a working explanation with a decorative image or pull quote that merely repeats it.

### Choose the form for the idea

Let the material determine the form:

- dialogue for ambiguity and scope;
- tables for repeated mappings or option comparisons;
- short prose for consequences and tradeoffs;
- code-shaped notation for class boundaries;
- diagrams for relationships and transitions;
- traces for correctness.

Vary paragraph and sentence length because the ideas require it, not as random decoration. Some decisions need one sentence. The main invariant may need several connected paragraphs.

## Phrases and constructions to audit

No punctuation mark or phrase proves AI authorship. The problem is repeated, low-information use. During the final edit, search for:

- em dashes used as the default join between unrelated clauses;
- repeated “not X, but Y” or “it is not just X; it is Y” framing;
- repeated openings such as “The key is,” “The important thing is,” or “It is worth noting”;
- generic scene-setting such as “In today's fast-paced world” or “Let's dive in”;
- inflated adjectives such as robust, seamless, comprehensive, powerful, scalable, or elegant without a measurable claim;
- vague transitions such as “With that in mind” when the next sentence can state the consequence directly;
- paragraphs that restate a heading before adding information;
- uniform three-item lists, uniform paragraph lengths, and repeated summary sections;
- repeated claims that a choice “ensures” an outcome without showing the invariant or test.

Keep an em dash when it is the clearest punctuation. Keep a contrast construction when both sides matter. Rewrite only formulaic repetition or empty emphasis.

## Concrete revision moves

Replace metacommentary with a domain fact:

- Weak: “The key is to make the system robust.”
- Better: “`dispense()` decrements stock only after payment covers the selected price.”

Replace abstract praise with a tradeoff:

- Weak: “This elegant approach is highly scalable.”
- Better: “The map makes product lookup constant-time on average, at the cost of maintaining one index.”

Remove throat-clearing:

- Weak: “Now that we have explored the requirements, let's dive into the class design.”
- Better: “The controller owns the purchase workflow; the slot owns quantity.”

Avoid mechanical negation:

- Weak: “This is not a payment system but a vending machine simulator.”
- Better: “Payment authorization stays outside the simulator. It accepts a confirmed amount.”

## Evidence and limits

Published authorship research supports looking beyond one token or punctuation habit. Human writing tends to show greater stylistic and discourse variation, while model output can be more homogenized; experienced readers also report using clusters of lexical and stylistic cues rather than a single marker. These are population-level observations, not reliable tests for one article:

- [Threads of Subtlety: Detecting Machine-Generated Texts Through Discourse Motifs](https://aclanthology.org/2024.acl-long.298/)
- [ChatGPT vs Human-authored Text: Insights into Controllable Text Summarization and Sentence Style Transfer](https://aclanthology.org/2023.acl-srw.1/)
- [People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text](https://aclanthology.org/2025.acl-long.267/)
- [Linguistic and Embedding-Based Profiling of Texts Generated by Humans and Large Language Models](https://aclanthology.org/2025.emnlp-main.1163/)

Do not promise detector evasion, manipulate text to fool a classifier, or inject random errors. The release goal is specific, accurate, varied, human-readable technical writing.

## Final read-through

Read the article once without code. Revise when:

1. two nearby paragraphs open the same way;
2. an adjective carries a claim that a scenario or test should prove;
3. a transition can be replaced by the actual consequence;
4. a design label appears without a counterexample;
5. an extension repeats the base design;
6. the conclusion merely recites all headings.

Then perform two more passes:

- **Continuity pass:** read the opening, section transitions, figure captions, and verification. Can a reader follow one question through to its answer? Remove an unexplained jump or a settled point that is needlessly reopened.
- **Scan pass:** read only headings and bold phrases, then inspect the rendered PDF. Do they locate the decisions without becoming a second full article? Check that bold is visibly bold and that diagrams remain legible at normal reading size.

For each extension, cover its prose and ask whether the sketch shows the actual new behavior. Then cover the sketch and ask whether the prose explains why the change is needed and what it costs. Both views must agree. These reviews require editorial judgment; a word count or format validator cannot prove coherence.
