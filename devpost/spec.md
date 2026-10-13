---
doc: spec
status: approved
---

# Exam-to-Quiz — Technical Spec

## How This Works, In Plain Language

This will be a local website written mainly in Python. Flask is the small Python web framework that receives actions from the browser and decides which page to show. HTML describes the page content, CSS gives the app its polished dark-and-cream appearance, and a small amount of JavaScript handles browser interactions such as quiz feedback and confirmation prompts.

SQLite will save the question bank, quiz attempts, answers, and progress in one local database file. This means the data remains after the app is closed, without requiring a separate database server or requiring the learner to edit JSON.

When the learner uploads a normal text-based PDF, Python reads the text directly with PyMuPDF. A parser then looks for the question statements, four answer choices, answer keys, and explanations in the extracted text. The learner sees a preview before anything is saved. If the format cannot be understood, the app shows an error and offers manual question entry rather than pretending the import succeeded.

This first version does not require an AI service or paid tokens. It focuses on reliably converting supported exam PDFs into a question bank. AI and OCR for scanned PDFs can be added later once the deterministic workflow is working.

## The Core Journey Through the System

1. The learner runs Flask and opens the local address in a browser. Flask serves the shared layout and the Overview page.
2. Overview asks the browser for saved statistics from Flask. Flask reads completed attempts from SQLite and renders the streak, accuracy, and practice calendar.
3. The learner opens Question Bank and selects a PDF. The browser sends the file to Flask.
4. Flask passes the file to the PDF extraction component. PyMuPDF returns text, and the question parser turns supported text patterns into temporary question records.
5. Flask renders the import preview. The preview is not saved yet.
6. The learner cancels or confirms. Cancel discards the temporary preview; confirmation validates and inserts the questions into SQLite.
7. The learner clicks **Quiz me** and chooses 5, 10, or 15. Flask checks the question count, selects and shuffles questions, and starts a quiz session.
8. The browser displays one question with four choices. The learner submits an answer to Flask, which compares it with the saved correct answer and returns feedback.
9. After the learner continues, the next question is displayed. When the selected count is reached, Flask saves the attempt and its answers to SQLite and renders the result.
10. Overview statistics and History now read the saved attempt. Selecting a history item loads its linked answers and shows the detailed review.

PRD ref: `prd.md > The Core Journey`, `prd.md > Features and Behavior`.

## Stack

- **Python 3.11+** — the learner's existing language; version availability should be checked early.
- **Flask 3.x** — local web framework for routes, templates, form handling, and sessions. Docs: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- **SQLite via Python's built-in `sqlite3` module** — persistent local storage without a separate server. Docs: [docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)
- **PyMuPDF (`fitz`)** — direct text extraction from normal PDFs without an AI API. Docs: [pymupdf.readthedocs.io](https://pymupdf.readthedocs.io/)
- **Jinja** — Flask's built-in HTML templating system. Docs: [jinja.palletsprojects.com](https://jinja.palletsprojects.com/)
- **Vanilla HTML, CSS, and JavaScript** — keeps the browser layer understandable and avoids a frontend build system. Docs: [developer.mozilla.org](https://developer.mozilla.org/)

The exact dependency versions should be pinned in `requirements.txt` after the first environment check. No external AI service is required for the POC.

## Where It Runs and How Someone Tries It

The app runs locally on the learner's computer in a Python virtual environment. A browser opens the local Flask address, normally `http://127.0.0.1:5000`.

Initial setup:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in a browser. The exact start command may become `python -m flask --app app run` if that better matches the final file structure.

For the demo recording, use a supported sample exam PDF, show its import preview, confirm it into the question bank, run a short quiz, submit an answer to show feedback, finish the quiz, and open the saved result in History. Deployment is optional; the hackathon still requires a short demo video and a public GitHub repository.

## Look and Feel

Implement `prd.md > Look and Feel` with:

- A dark background and cream text.
- Clean modern sans-serif typography.
- Generous whitespace and clear visual hierarchy.
- A restrained accent palette, with tasteful gradients or geometric details where they improve the layout.
- Clearly styled primary actions for **Quiz me**, **+ Add Questions**, and **Add Questions to Database**.
- Green feedback for correct answers and a restrained error color for incorrect answers or import failures.
- Responsive layout that remains usable on a phone-sized viewport.

The interface should feel like a professional modern study product, not a raw HTML prototype or a dense admin dashboard.

## Components

### Flask application and routes

Owns the page routes and form submissions for Overview, Question Bank, History, import preview, quiz setup, quiz answers, results, and database clearing. It coordinates the other components and returns explicit success or error pages/messages.

PRD ref: `prd.md > Screens and Layout`, `prd.md > Features and Behavior`.

### Shared layout and navigation

Provides the top navigation for Overview, Question Bank, and History plus consistent page structure and responsive styling.

PRD ref: `prd.md > Screens and Layout > Shared navigation`.

### Overview statistics

Queries saved quiz attempts and calculates day streak, daily accuracy, weekly accuracy, and the practice calendar. It renders an understandable empty state when no quizzes exist.

PRD ref: `prd.md > Screens and Layout > Overview`, `prd.md > Features and Behavior > Progress, history, and persistence`.

### Question Bank management

Lists saved questions, accepts PDF uploads, launches manual entry, previews extracted questions, confirms or cancels imports, deletes individual questions after confirmation, and starts the clear-database confirmation flow.

PRD ref: `prd.md > Screens and Layout > Question Bank`, `prd.md > Screens and Layout > Import preview`, `prd.md > Screens and Layout > Manual question entry`, `prd.md > Features and Behavior > Adding and reviewing questions`.

### PDF text extraction and question parser

Reads text-based PDFs with PyMuPDF and converts supported exam formatting into temporary question records. It must reject or report unsupported input clearly; it must not silently create incomplete questions.

PRD ref: `prd.md > Features and Behavior > Adding and reviewing questions`.

### Quiz engine

Validates the requested count, selects a random set, tracks the current question and submitted answers, compares answers with the question bank, and returns per-question feedback.

PRD ref: `prd.md > Screens and Layout > Quiz setup`, `prd.md > Screens and Layout > Quiz question and feedback`, `prd.md > Features and Behavior > Starting and completing a quiz`.

### Results and history

Calculates score and percentage, saves each completed attempt, lists summaries, and loads the detailed question-and-feedback review for a selected attempt.

PRD ref: `prd.md > Screens and Layout > Quiz results`, `prd.md > Screens and Layout > History and detailed review`, `prd.md > Features and Behavior > Progress, history, and persistence`.

### Persistence layer

Creates the SQLite schema, inserts and reads questions and attempts, and performs database clearing only after explicit confirmation.

PRD ref: `prd.md > Features and Behavior > Progress, history, and persistence`, `prd.md > Features and Behavior > Clearing the question bank`.

### Manual entry and recovery UI

Provides a form for one question with four choices, the correct answer, and an explanation. It is the fallback when a file cannot be parsed or when the learner wants to add a question directly.

PRD ref: `prd.md > Features and Behavior > Adding and reviewing questions`, `prd.md > States and Boundaries`.

## Data Model

SQLite database file: `data/exam_to_quiz.sqlite3`.

### questions

- `id` — primary key.
- `question_text` — question statement.
- `choice_a`, `choice_b`, `choice_c`, `choice_d` — the four answer choices.
- `correct_choice` — one of A, B, C, or D.
- `explanation` — feedback shown after submission.
- `source_name` — uploaded filename or `manual`.
- `created_at` — saved timestamp.

### quiz_attempts

- `id` — primary key.
- `question_count` — 5, 10, or 15.
- `correct_count` — number answered correctly.
- `percentage` — calculated result.
- `started_at` and `completed_at` — timestamps used by History and Overview.

### attempt_questions

- `id` — primary key.
- `attempt_id` — link to `quiz_attempts`.
- `question_id` — link to `questions`.
- `question_order` — order used in the attempt.
- `selected_choice` — learner's submitted choice.
- `is_correct` — saved result.

Question text is stored in the question bank, while each attempt stores a link to the question plus the learner's answer and order. This avoids copying the full question into every history item while preserving the completed quiz review. If a future editor changes a question, the build should either preserve the original attempt snapshot or document that historical reviews use the current question text; this is an implementation issue to settle during build testing.

## File Structure

```text
project/
├── app.py                         # Flask entry point and route registration
├── requirements.txt               # Pinned Python dependencies
├── data/
│   └── .gitkeep                   # SQLite file is created locally and ignored
├── instance/
│   └── .gitkeep                   # Optional Flask instance-data location
├── db/
│   ├── __init__.py                # Database package
│   ├── connection.py              # SQLite connection and schema setup
│   └── queries.py                 # Question, attempt, and statistics operations
├── services/
│   ├── __init__.py
│   ├── pdf_extractor.py           # PyMuPDF text extraction
│   ├── question_parser.py         # Supported exam-format parsing and validation
│   └── quiz_service.py            # Selection, scoring, and attempt coordination
├── templates/
│   ├── base.html                  # Shared navigation and page shell
│   ├── overview.html              # Overview dashboard
│   ├── question_bank.html         # Bank list and actions
│   ├── import_preview.html        # Extracted-question review
│   ├── manual_question.html       # Manual fallback form
│   ├── quiz_setup.html            # 5/10/15 selection
│   ├── quiz_question.html         # Question and feedback
│   ├── quiz_result.html            # Score and next actions
│   ├── history.html               # Saved attempt summaries
│   ├── history_detail.html        # Detailed past attempt
│   └── error.html                 # Clear recovery messages
├── static/
│   ├── css/
│   │   └── style.css              # Dark/cream responsive styling
│   └── js/
│       └── app.js                 # Small UI interactions and confirmations
├── tests/
│   ├── test_parser.py             # Supported PDF-text parsing cases
│   ├── test_quiz.py               # Selection and scoring behavior
│   └── test_routes.py             # Key page and error flows
└── devpost/                       # Planning documents
```

The database file and any uploaded personal study materials must not be committed. A secret-free `.env.example` may document future configuration, but no credential should be placed in the repository.

## External Services and Dependencies

There are no required external services for the POC. PyMuPDF is a local library, and SQLite is built into Python.

Possible later AI/OCR service:

- **Purpose:** understand scanned/image-only PDFs or generate explanations and question variations.
- **Status:** deferred; not required for the first demo.
- **Reason:** hosted APIs require keys, have changing free quotas, and add a failure and privacy boundary. A local model would avoid token charges but add installation and hardware complexity.
- **If added later:** use a server-side provider adapter, keep the key in a local environment variable, validate structured responses before saving, and provide a deterministic/manual fallback.

## Important Failure Modes

- **PDF has no extractable text or unsupported formatting** → show an explicit import error, explain that the file could not produce usable questions, and offer another file or manual entry.
- **Question bank has fewer questions than requested** → show the available/required counts and direct the learner to Question Bank instead of starting a partial quiz.
- **Database cannot be opened or saved** → show a clear error and do not claim the import or result was saved.
- **Learner cancels an import or database clear** → leave existing saved data unchanged.
- **Learner deletes a question** → require confirmation before removing only that question; cancellation leaves it unchanged.
- **No saved questions or history** → show clear empty states with the next useful action.

## What Was Simplified and Why

- **Text-based PDF extraction** instead of AI extraction and OCR — avoids paid tokens and makes the first kernel predictable; scanned PDFs and complex layouts need a later extraction layer.
- **One four-choice MCQ format** instead of every exam question type — keeps parser and quiz behavior demonstrable within the hackathon.
- **Local Flask and SQLite** instead of hosted infrastructure and accounts — keeps setup, cost, privacy, and debugging manageable while satisfying the demo requirement.
- **A simple manual-entry form** instead of a full question editor — provides a usable safety net without building a second product.
- **Individual deletion** instead of editing — makes testing and cleanup possible without expanding the Question Bank into a full editor.
- **Derived Overview statistics** instead of a separate analytics system — saved attempts provide enough data for streaks, accuracy, and the practice calendar.

## Decisions and Open Issues

### Decisions

- Learner accepted a local Flask web app because Python is familiar and they want each part explained.
- Learner chose SQLite because persistence is important and they are willing to learn a more robust option than a plain data file.
- Learner agreed to deterministic PDF text extraction without a required AI service for the first version after learning that normal PDFs can be read directly.
- The architecture keeps AI/OCR optional and later rather than making the demo depend on free-tier quotas.
- The app runs locally for the demo; deployment is optional.

### One useful unknown clarified

The learner was unsure whether PDF reading required AI or paid tokens. We clarified that normal text-based PDFs can be read locally with PyMuPDF, while scanned PDFs and generated explanations may need OCR or AI later. The first build should test this assumption with a representative exam PDF before adding any AI dependency.

### Open issues

- **Must check early in build:** whether the learner's sample PDFs have extractable text and a consistent enough format for the parser.
- **Must check early in build:** the exact supported question and answer-key patterns; unsupported formats must produce a visible error.
- **Can wait until build investigation:** whether historical reviews need immutable question snapshots before any editing feature exists.
- **Deferred:** AI extraction, OCR, generated variations, and online answer verification.
