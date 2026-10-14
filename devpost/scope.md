---
doc: scope
status: approved
---

# Exam-to-Quiz

Turn exam PDFs into a reusable quiz and feedback experience for active learning.

## The Unique Kernel

Upload ordinary exam PDFs instead of manually entering every question. The app converts the available exam questions and answer information into a reusable internal question bank, then presents them with immediate feedback and explanations. The technical storage format will be chosen later; the learner does not need to know HTML or JSON to use the app.

## Who It's For

A first-year Computer Engineering student studying content-heavy courses. They want to test their understanding actively instead of passively memorizing lecture content, but their school provides only a limited number of past papers and tutorials.

The first user is the learner themself, with close friends as possible early users if the result is reliable.

## The Core Loop

The learner provides exam material and, where useful, lecture slides as content reference. They click **Quiz me**, which selects a random set of a chosen length, such as 10, 20, or 30 questions, and presents one randomly ordered MCQ at a time. They submit each choice and immediately see whether it was correct, the correct answer, and an explanation. They continue until the selected number of questions is complete, then see a score and basic strengths and weaknesses.

## Inspiration & Identity

The product should feel like a polished, focused study website rather than a raw HTML prototype or a manually assembled data tool. It should support the learner's active-learning goal: practice recalling and applying concepts, not just rereading lecture content.

The learner previously experimented with Gemini Canvas but found the manual question-data setup, raw HTML, and lack of polish too slow. A friend's quick Claude Artifacts prototype inspired the desire for a more polished result.

## Why This Matters to the Learner

Automating quiz creation could prevent the learner from running out of practice material after completing the small set of school-provided past papers and tutorials. They want a useful final product and want to learn how to use AI in coding while building it.

## What "Working" Looks Like

For a one-minute demo, the learner loads exam material, chooses a short quiz length, and clicks **Quiz me**. The app presents questions in their original MCQ styles, displays the correct answer and an explanation after each submission, and continues until the selected set is complete. It then shows a final score and basic performance information.

The compelling proof is that an exam PDF has become a usable quiz-and-feedback experience without manually writing a question database.

## The POC Boundary

The proof of concept will focus on:

- Exam material and MCQ-style exam questions.
- Converting exam questions into the reusable question-bank data the app needs, without requiring the learner to hand-author a technical data format.
- A single **Quiz me** flow with a chosen quiz length, such as 10, 20, or 30 questions, that presents one randomly ordered question at a time.
- Answer submission with the correct answer and an explanation immediately afterward.
- A short quiz result with a score and simple topic or question performance.
- A web experience that is usable on the learner's computer and reasonably responsive on a phone.

The first version may use a prepared or locally loaded question bank if fully automatic PDF parsing cannot be made reliable within the hackathon time. The conversion workflow remains the kernel to demonstrate and improve.

## Later

- Generate mostly new questions and variations rather than only reproducing exam questions.
- Extract questions from images as well as PDF files.
- Use lecture slides and, where appropriate, online sources to infer and verify answers for generated questions.
- Similar-question generation.
- Topic-specific, timed, and weak-spot quizzes.
- More detailed progress tracking, editable question-bank management, and long-term learning history.
- Switching between separate subject question banks, so the learner can study different courses from the same app.
- Flashcards and broader subject support, including math and coding formats.
- Stronger mobile experience and sharing with friends or other students.

## Explicitly Cut

- Supporting every subject in the first version: math and coding require specialized calculation and formatting support.
- Building every quiz mode at once: one random **Quiz me** mode is enough to prove the core loop.
- Full automatic answer inference and online verification in the first version: correctness and external-source integration would add reliability and research complexity before the basic workflow is proven.
- A complete production-grade account and synchronization system: it is not needed to demonstrate the learning experience.
- A full manual question editor: useful later, but it would distract from the PDF-to-quiz kernel.
