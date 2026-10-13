# Exam-to-Quiz: Next Agent Handoff

This project completed the Build With AI: Basics planning and build workflow. The current implementation is a working proof of concept. Continue normally after the hackathon: the limitations below are priorities and tradeoffs, not permanent restrictions.

## Current state

- Local Flask app in `app.py`.
- SQLite database created at `instance/exam_to_quiz.sqlite3`.
- PDF text extraction with PyMuPDF.
- Strict parser for supported numbered four-choice MCQ text.
- Editable import preview before confirmation.
- Manual question entry fallback.
- Random 5/10/15-question quizzes with answer feedback and explanations.
- Persistent History, detailed review, Overview accuracy, streak, and calendar.
- Individual question deletion and whole-bank deletion with confirmation.
- Tests: run `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.
- Demo sample: `sample_exam.pdf`.

## Start here

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

Read `devpost/app-map.html` for the main code route. Read `devpost/prd.md` and `devpost/spec.md` for the product decisions and technical rationale. The `devpost/` planning files document the original hackathon boundary; this handoff is permission to expand beyond it after preserving a working baseline.

## Recommended next work

1. Improve PDF parsing to support real exam layouts, answer keys separated from questions, multi-line choices, and scanned PDFs.
2. Add import deduplication or an explicit replace/merge choice so repeated imports do not create confusing duplicate questions.
3. Add subject/question-bank management.
4. Add topic tags and topic-specific quizzes.
5. Add generated question variations only after establishing answer-quality validation.
6. Add richer weak-topic analytics and timed quizzes.
7. Consider an AI/OCR provider behind a small adapter with local environment configuration and a deterministic manual fallback. Never commit API keys.
8. Add immutable history snapshots before building question editing inside the saved bank, so old reviews cannot silently change.
9. Add authentication, cloud storage, and deployment only when multi-device use or sharing is a real requirement.

## Important known limitations

- The parser is intentionally strict and does not yet handle every PDF.
- AI is not required or connected; normal text extraction is local and free.
- History links to current question rows. If saved questions become editable, add snapshots or versioning first.
- The app uses a development secret key and local storage; do not deploy this exact configuration publicly.
- `sample_exam.pdf` contains fictional practice content for local testing.

## Working agreements for future changes

- Run the full test command before and after meaningful changes.
- Add a regression test for each parser, quiz, persistence, or safety behavior.
- Preserve the learner-facing core loop: upload/import, inspect or edit, confirm, quiz, feedback, result, history.
- Keep credentials in local `.env` files; `.env` and `.env.*` are ignored, while `.env.example` is allowed.
- Inspect staged files for secrets and personal learning context before committing.
- Keep public-safe documentation separate from `devpost/learner-profile.md`, which is intentionally ignored.
