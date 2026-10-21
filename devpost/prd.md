---
doc: prd
status: approved
---

# Brainoe — Product Requirements

Turn exam materials into a reusable MCQ practice and feedback experience for students.
Source: `scope.md > The Unique Kernel`, `scope.md > The Core Loop`

## The Core Journey

1. The learner opens the app on the **Overview** page. A top navigation bar provides **Overview**, **Question Bank**, and **History**.
2. Overview shows the learner's current practice statistics and a prominent **Quiz me** button.
3. The learner clicks **Quiz me** and chooses a quiz length of 5, 10, or 15 questions.
4. The app selects a random set of questions and presents them in random order, one at a time.
5. Each question shows its statement and four answer choices labeled A–D. The learner selects an answer and submits it.
6. The app shows whether the answer was correct, the correct answer, and an explanation before allowing the learner to continue.
7. The learner repeats the question-and-feedback cycle until the selected number of questions is complete.
8. The app shows the final score out of the total and the percentage correct, with buttons for **Home** and **Another quiz**. **Another quiz** starts a new quiz using the same question-count setting.
9. The completed quiz is saved. The learner can later find its date, time, and result in **History**, then open a detailed review containing the questions, their answers, the correct answers, and explanations.

Source: `scope.md > The Core Loop`, `scope.md > What "Working" Looks Like`

## Screens and Layout

### Shared navigation

A top bar is visible across the main app pages and links to:

- **Overview** — the home page and starting point for a quiz.
- **Question Bank** — imported questions, adding questions, manual entry, individual deletion, and database clearing.
- **History** — completed quiz summaries and detailed past-quiz review.

### Overview

The page has a polished dashboard-like layout with:

- Day streak: consecutive days on which the learner practiced.
- Daily question accuracy.
- Weekly question accuracy.
- A calendar chart where each small square is green for a day with practice and grey for a day without practice.
- A prominent **Quiz me** button.

### Question Bank

The page provides access to the current reusable question bank and a prominent **+ Add Questions** button. Each question can be deleted individually after confirmation. It also provides a **Clear Database** action that requires explicit confirmation before deletion.

### Import preview

After a learner selects an input file, the app shows the extracted questions, answer choices, correct answers, and explanations for review. The learner can choose **Cancel X** to discard the preview or **Add Questions to Database** to append the reviewed questions to the question bank.

### Manual question entry

The Question Bank includes a simple fallback form for entering a question, four answer choices, the correct answer, and an explanation when an uploaded file cannot produce usable questions or when the learner wants to add a question directly.

### Quiz setup

Clicking **Quiz me** opens a compact selection control containing exactly three choices: 5, 10, or 15 questions.

### Quiz question and feedback

The quiz screen shows the question number, question statement, four answer choices labeled A–D, and a submission action. After submission, it shows the correctness result, correct answer, and explanation. The learner then proceeds to the next question.

### Quiz results

After the selected number of questions, the result view shows the score in the form `3/5` and the percentage in the form `60%`. It provides **Home** and **Another quiz** actions.

### History and detailed review

History starts empty when no quizzes have been completed. Each saved quiz summary includes its date, time, and result. Selecting a summary opens a detailed review of all questions in that quiz, including the learner's answer, correct answer, and explanation.

Source: `scope.md > The POC Boundary`

## Look and Feel

The app should feel professional and modern rather than like a raw or obviously improvised prototype. It should take inspiration from Canva's modern presentation style:

- Clean, contemporary sans-serif typography.
- Generous whitespace and uncluttered layouts.
- A dark background with cream-colored text.
- A restrained set of accent colors, with tasteful gradients or geometric elements where useful.
- Clear hierarchy so the quiz action, question choices, feedback, and results are easy to find.

The visual direction should support focused active learning rather than feel like a dense analytics dashboard.

## Features and Behavior

### Adding and reviewing questions

- The learner can choose a file from the Question Bank page.
- The app attempts to extract MCQ questions, four choices, correct answers, and explanations.
- Extracted content appears in a reviewable preview before changing the question bank.
- Each extracted question can be corrected in the preview before confirmation.
- **Cancel X** discards the preview without changing the question bank.
- **Add Questions to Database** appends the previewed questions to the existing question bank.
- If no usable questions are extracted, the app shows an understandable error and recovery guidance, including trying another file or using manual entry.
- The learner can manually enter a question, four choices, correct answer, and explanation as a safety net.
- The learner can delete an individual question after confirming the destructive action.

Acceptance criteria:

- A successful import visibly shows extracted questions before they are added.
- Editing a question in the preview changes the version that is added after confirmation.
- Cancelling leaves the existing question bank unchanged.
- Confirming an import makes the questions available to **Quiz me**.
- An unusable file produces an error state rather than a misleading empty success state.
- Manual entry produces a question that can be used in a quiz.
- Cancelling an individual deletion leaves the question in the bank; confirming removes only that question and shows a result message.

### Starting and completing a quiz

- **Quiz me** offers only 5, 10, and 15 as question-count choices.
- The app randomly selects and orders questions from the question bank.
- A quiz question displays one statement and four answer choices labeled A–D.
- The learner must submit an answer before moving forward.
- Feedback appears after submission and includes correctness, the correct answer, and an explanation.
- The quiz continues until the selected question count is complete.
- Results show score and percentage, then offer **Home** and **Another quiz**.
- **Another quiz** starts another quiz with the previous question-count setting.

Acceptance criteria:

- A 5-question quiz ends after exactly 5 questions, and likewise for 10 and 15.
- The score numerator equals the number of correct submitted answers.
- The displayed percentage matches the score.
- No question is skipped before feedback is shown.

### Progress, history, and persistence

- Completed quizzes remain available after the learner closes and reopens the app.
- Overview statistics are calculated from saved practice results.
- History lists completed quizzes with date, time, and score percentage.
- Opening a history item shows the full question-and-feedback review for that quiz.
- History and statistics begin in an empty state when no quizzes have been taken.

Acceptance criteria:

- Completing a quiz creates one visible History item.
- Reopening the app preserves the question bank, history, and overview data.
- Selecting a History item opens the corresponding questions, learner answers, correct answers, and explanations.

### Clearing the question bank

- **Clear Database** is available from Question Bank.
- Activating it opens a confirmation prompt explaining that the question bank will be deleted.
- The destructive confirm button is red.
- The cancel button is grey and leaves the question bank unchanged.
- Clearing removes the available question bank but does not silently pretend the action was cancelled.

## States and Boundaries

- **First use / empty Question Bank** — explain that questions must be added before a quiz can start and provide a path to add questions.
- **Too few questions** — if the learner requests 5, 10, or 15 but the bank contains fewer questions, explain the shortfall and direct them to Question Bank to add more questions.
- **No usable extracted questions** — show an error describing the problem and suggest trying another file or using manual entry.
- **Individual question deletion** — require confirmation before removing one question; cancellation leaves it unchanged.
- **Import preview** — extracted questions are temporary until the learner cancels or confirms the addition.
- **Empty History** — show a clear no-quizzes-yet message rather than an empty unexplained list.
- **Quiz in progress** — require an answer submission before advancing; the selected question count remains fixed for that quiz.
- **Completed quiz** — save the result and detailed answers so it is available in History.
- **Clear confirmation** — deletion requires an explicit confirmation; cancel preserves the bank.
- **Persistence** — the question bank, quiz history, and derived overview statistics remain after closing and reopening the app.
- **POC input boundary** — the first version focuses on exam-style MCQs with four choices. More varied question types, image input, subject switching, and generated variations are deferred.

## Product Decisions

- Start with a single random **Quiz me** flow and question counts of 5, 10, or 15 to keep the proof of concept focused.
- Show per-question correctness, answer, and explanation before moving on because the tool is intended to support active learning.
- Preview extracted questions before appending them so the learner can inspect what was understood.
- Include manual question entry as a safety net so the app remains usable when file extraction fails.
- Include individual deletion so imported or manual questions can be cleaned up during testing.
- Persist the question bank, statistics, and history across sessions because progress should remain useful after closing the app.
- Add a History page with detailed review so prior learning attempts can be revisited.
- Use a dark, professional, modern visual style with cream text, inspired by Canva's clean presentation layouts.
- Keep topic, difficulty, question-type selection, advanced analytics, and other quiz modes out of the first version to protect the proof-of-concept boundary.

## What We're Building

- A three-area web experience with Overview, Question Bank, and History navigation.
- A persistent question bank populated through file import preview and manual entry, with individual deletion.
- A 5-, 10-, or 15-question randomized MCQ quiz.
- Per-question feedback with correct answer and explanation.
- Final score and percentage.
- Persistent quiz history with detailed review.
- Overview streak, accuracy, and practice-calendar statistics.
- Clear empty, insufficient-question, import-error, and destructive-confirmation states.

## Deferred From the POC

- Topic, difficulty, and question-type filters: these add quiz configuration complexity beyond the single random flow.
- Generated variations and similar questions: the first version proves import and practice using existing exam questions.
- Image-to-question extraction: useful for photographed or scanned material, but not required for the first import workflow.
- Switching between separate subject banks: the first version establishes one reusable bank experience before adding subject management.
- Flashcards, timed quizzes, weak-spot quizzes, and richer topic analytics: these are later learning modes, not needed to prove the core loop.
- Accounts, cloud sync, and sharing: persistence is needed, but a multi-user system is outside the proof of concept.
- FAQ and advanced troubleshooting: clear inline recovery guidance is sufficient initially.

## Possible Later Enhancements

- Generate new question variations from existing material and lecture content.
- Support images and scanned pages as question sources.
- Add subject selection, topic filters, difficulty, timed quizzes, weak-spot quizzes, and flashcards.
- Add richer progress analysis and sharing with friends.

## Non-Goals

- Supporting every subject, especially math and coding, in the first version.
- Automatically verifying answers with online sources in the first version.
- Building a full production account system or collaborative platform.
- Requiring the learner to understand or manually edit the internal storage format.

## Open Questions

- **Before `4-spec`:** What PDF input path and AI approach can provide a reliable demo within available cost and time limits?
- **Before `4-spec`:** Should the first demo use a real upload flow, a prepared sample file, or support both?
- **Can wait until build investigation:** The exact visual accent colors and the precise layout of the statistics cards.
- **Can wait until build investigation:** How much extracted content can be edited in the preview before confirmation.
