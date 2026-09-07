# Research-grounded interviewer questions

Read this file before drafting questions the candidate can ask at the end of an interview.

## Purpose

Create 5-6 questions that help the candidate understand the work, the company's current challenges, and how the team solves problems. The questions should also show informed interest without pretending to know internal details.

Use `company-context.md` and `job-analysis.md` as the factual basis. At least four questions must be traceable to a specific company, product, customer, technical, operating, or role signal found during research.

## Question mix

Prioritize questions about:

- the most important problem the team is trying to solve now;
- the work or customer outcome this role will influence;
- technical or product constraints that make the problem difficult;
- how the team evaluates tradeoffs and makes decisions with incomplete information;
- how engineers investigate failures, learn from incidents, or change their approach;
- what strong performance looks like in the first months;
- how the problem or product is likely to evolve.

Most of the set should focus on the company's work and challenges. One or two questions may focus on role expectations, collaboration, or growth when they connect directly to those challenges.

## Writing rules

- Ask open-ended questions that invite a substantive answer.
- Keep each question concise and easy to say aloud.
- Refer to a verified company signal without reciting a press release or marketing phrase.
- Phrase uncertain context as a question, not as a claim.
- Avoid questions already answered clearly by the job description or company website.
- Avoid compensation, benefits, leave, and administrative questions unless the user requests them.
- Avoid generic prompts such as `What is the culture like?` or `What does a typical day look like?`
- Do not ask for confidential roadmaps, customer data, incident details, or competitive information.
- Avoid em dashes, staged `not X but Y` contrasts, and performative or flattering language.

## Adapt to the interviewer

If the interviewer type is known, adjust the questions:

- **Hiring manager or technical lead:** priorities, architecture, tradeoffs, success measures, and team constraints.
- **Engineer or peer:** daily problem-solving, code ownership, incidents, reviews, and collaboration.
- **Product or cross-functional partner:** customer problems, prioritization, feedback, and engineering-product tradeoffs.
- **Recruiter:** client identity, role scope, process, and information the recruiter can verify. Do not expect detailed architecture answers.

Do not create interviewer questions in anonymous-company mode. That mode is limited to a role-focused cover letter and tailored resume.

## Output format

Create `interviewer-questions.md` with this structure:

```markdown
# Interviewer Questions

## Questions to ask

1. <question>
2. <question>
3. <question>
4. <question>
5. <question>

## Research grounding

| Question | Company or role signal | Source |
| --- | --- | --- |
| 1 | <concise signal> | <company-context section or direct source URL> |
```

Use six questions only when the research supports six distinct, useful lines of inquiry. The grounding table is for the candidate's preparation and can be omitted when copying the questions into personal notes.
