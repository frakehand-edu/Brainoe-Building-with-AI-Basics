---
doc: checklist
status: approved
---

# Build Checklist

Build mode: learn

## Slices

- [x] **1. You can open the polished app and add a manual question**
  Becomes usable: A running Flask app with Overview, Question Bank, and History navigation; a manual question can be saved and appears in the question bank.
  Why now: Bootstraps the full app and proves the first end-to-end path with a reliable data source before PDF parsing.
  PRD ref: `prd.md > The Core Journey` (steps 1-2), `prd.md > Features and Behavior > Adding and reviewing questions`
  Spec ref: `spec.md > How This Works, In Plain Language`, `spec.md > Components > Flask application and routes`, `spec.md > Components > Persistence layer`, `spec.md > Look and Feel`
  Build: Scaffold the Flask app, SQLite schema and queries, shared templates, responsive dark/cream styling, navigation, Overview empty state, Question Bank page, and manual question-entry form.
  Verify (mechanical): Create the virtual environment, install dependencies, run the app, and use a Flask test request or browser smoke check to confirm the three pages load and a manual question is persisted and listed.
  Learner check: Open the local app, visit all three navigation tabs, add a manual four-choice question, and say whether the visual direction and page structure feel like the product you pictured.
  Commit: `Build app shell and manual question entry`

- [x] **2. You can upload a PDF and preview extracted questions**
  Becomes usable: A supported text-based exam PDF is uploaded and produces a preview showing question text, four choices, correct answer, and explanation without changing the saved bank until confirmation.
  Why now: Proves the unique PDF-to-question-bank kernel early and exposes real PDF-format risks before quiz work depends on it.
  PRD ref: `prd.md > Screens and Layout > Import preview`, `prd.md > Features and Behavior > Adding and reviewing questions`
  Spec ref: `spec.md > Components > PDF text extraction and question parser`, `spec.md > Important Failure Modes`
  Build: Add PyMuPDF extraction, a validated parser for the supported exam format, upload handling, preview rendering, cancel behavior, and clear unsupported/no-question errors.
  Verify (mechanical): Run parser tests against a representative text-based PDF fixture and an invalid/unsupported fixture; confirm extracted records have four choices and a valid answer before the preview route renders.
  Learner check: Upload a sample PDF, inspect the extracted preview, cancel once to confirm the bank is unchanged, then upload it again and report whether the extracted content matches the source.
  Commit: `Add PDF extraction preview`

- [ ] **3. You can confirm questions and run a complete quiz**
  Becomes usable: Confirmed questions become available to Quiz me; the learner can choose 5, 10, or 15 when enough questions exist, answer each question, see feedback and explanation, and reach a score.
  Why now: Connects the imported kernel to the core active-learning loop and creates the first compelling demo journey.
  PRD ref: `prd.md > The Core Journey` (steps 3-8), `prd.md > Features and Behavior > Starting and completing a quiz`
  Spec ref: `spec.md > Components > Quiz engine`, `spec.md > Components > Results and history`
  Build: Add preview confirmation, quiz setup validation, randomized selection, quiz session state, question screen, submission feedback, next-question flow, result score/percentage, Home, and Another quiz.
  Verify (mechanical): Run scoring and route tests for a 5-question quiz, including correct and incorrect answers, exact completion count, feedback-before-next behavior, and insufficient-question rejection.
  Learner check: Import or add enough questions, run a 5-question quiz, intentionally get one answer wrong, and confirm the feedback, final score, and Another quiz behavior.
  Commit: `Connect question bank to quiz flow`

- [ ] **4. You can review saved history and progress after reopening**
  Becomes usable: Completed quizzes persist across a restart, appear in History with date/time/result, open into a detailed review, and update Overview statistics and calendar.
  Why now: Adds the persistence value that makes repeated active practice useful beyond one session.
  PRD ref: `prd.md > Screens and Layout > Overview`, `prd.md > Screens and Layout > History and detailed review`, `prd.md > Features and Behavior > Progress, history, and persistence`
  Spec ref: `spec.md > Data Model`, `spec.md > Components > Overview statistics`, `spec.md > Components > Results and history`
  Build: Save attempts and answer links, render history summaries and detailed reviews, calculate streak/accuracy/calendar values, and handle empty states.
  Verify (mechanical): Complete a quiz, stop and restart Flask, confirm the question bank, history item, detailed answers, score, and Overview statistics remain available.
  Learner check: Close and reopen the app, open History and a completed attempt, then inspect Overview and tell me what feels clear or confusing.
  Commit: `Persist quiz history and progress`

- [ ] **5. You can safely manage the question bank**
  Becomes usable: The learner can clear the question bank only after an explicit confirmation and can recover from failed imports through manual entry.
  Why now: Completes the important safety and recovery states without adding deferred features such as AI, OCR, filters, or accounts.
  PRD ref: `prd.md > Features and Behavior > Clearing the question bank`, `prd.md > States and Boundaries`
  Spec ref: `spec.md > Components > Manual entry and recovery UI`, `spec.md > Important Failure Modes`
  Build: Add the red delete/grey cancel confirmation, clear-data behavior, no-usable-question recovery guidance, and final visual polish for the demo path.
  Verify (mechanical): Test cancel and confirm branches independently, confirm clearing removes questions but preserves the app, and confirm an unusable upload shows recovery actions without saving partial data.
  Learner check: Trigger Clear Database and cancel, trigger it again and confirm, then try an unusable file and use manual entry to restore one usable question.
  Commit: `Add question bank safety and recovery`

## Hands-on Checkpoints

- [ ] Early usable behavior explored — after Slice 1, review the app shell and manual-entry experience before parser and quiz work.
- [ ] Final kick-the-tires exploration and feedback completed

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship

## Code Tour and App Map

- [ ] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence:
Route and stops:
Edit outcome:
Reflection:
Activity mode:

## Revisions

- Slice 1 feedback changed the Overview **Quiz me** route to explain when fewer than five questions exist and added an interim setup page for the already-populated case; the full quiz setup remains in Slice 3 as planned. Visual feedback also added active navigation pills, a brain mark, stronger calendar spacing, and cream text on the Overview card.
- Follow-up visual feedback enlarged and integrated the Overview card copy so it follows the card's angled presentation instead of looking like detached labels.
- Slice 3 feedback keeps imported questions in insertion order, uses an error-colored cancellation notice, and adjusts quiz question/choice typography for readability.
