import tempfile
import unittest
from pathlib import Path
from io import BytesIO

from app import create_app
from services.question_parser import parse_questions


class AppSmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        app = create_app()
        self.app = app
        app.config.update(
            TESTING=True,
            DATABASE=Path(self.temp_dir.name) / "test.sqlite3",
        )
        from db.connection import init_db

        init_db(app.config["DATABASE"])
        self.client = app.test_client()

    def tearDown(self):
        from db.connection import close_db

        with self.app.app_context():
            close_db()
        self.temp_dir.cleanup()

    def test_main_pages_load(self):
        for path in ("/", "/question-bank", "/history", "/question-bank/manual"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Brainoe", response.data)
            self.assertNotIn(b"Exam-to-Quiz", response.data)

    def test_manual_question_is_persisted(self):
        response = self.client.post(
            "/question-bank/manual",
            data={
                "question_text": "What is active recall?",
                "choice_a": "A study method",
                "choice_b": "A file format",
                "choice_c": "A database",
                "choice_d": "A browser",
                "correct_choice": "a",
                "explanation": "It asks you to retrieve knowledge from memory.",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"What is active recall?", response.data)

    def test_quiz_me_explains_when_bank_is_too_small(self):
        response = self.client.get("/quiz", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You need at least 5 questions", response.data)

    def test_question_parser_reads_supported_format(self):
        questions = parse_questions(
            """Question 1. Which answer is correct?
A) First
B) Second
C) Third
D) Fourth
Answer: C
Explanation: The third answer is correct.
"""
        )
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]["correct_choice"], "c")
        self.assertEqual(questions[0]["choices"][2], "Third")

    def test_pdf_upload_shows_preview_without_saving(self):
        import fitz

        document = fitz.open()
        page = document.new_page()
        page.insert_text(
            (72, 72),
            "Question 1. Which answer is correct?\nA) First\nB) Second\nC) Third\nD) Fourth\nAnswer: C\nExplanation: The third answer is correct.",
        )
        pdf_bytes = document.tobytes()
        document.close()
        response = self.client.post(
            "/question-bank/import",
            data={"question_file": (BytesIO(pdf_bytes), "sample.pdf")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Import preview", response.data)
        self.assertIn(b"Which answer is correct?", response.data)
        self.assertNotIn(b"Which answer is correct?", self.client.get("/question-bank").data)

    def test_preview_edits_are_saved_before_confirmation(self):
        import fitz

        document = fitz.open()
        page = document.new_page()
        page.insert_text(
            (72, 72),
            "Question 1. Which answer is correct?\nA) First\nB) Second\nC) Third\nD) Fourth\nAnswer: C\nExplanation: The third answer is correct.",
        )
        pdf_bytes = document.tobytes()
        document.close()
        self.client.post(
            "/question-bank/import",
            data={"question_file": (BytesIO(pdf_bytes), "sample.pdf")},
            content_type="multipart/form-data",
        )
        response = self.client.post(
            "/question-bank/import/edit",
            data={
                "question_0_text": "Edited question",
                "question_0_choice_a": "Edited first",
                "question_0_choice_b": "Edited second",
                "question_0_choice_c": "Edited third",
                "question_0_choice_d": "Edited fourth",
                "question_0_correct": "b",
                "question_0_explanation": "The edited second answer is correct.",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Edited question", response.data)
        confirmed = self.client.post(
            "/question-bank/import/confirm",
            follow_redirects=True,
        )
        self.assertIn(b"Edited question", confirmed.data)
        self.assertIn(b"Edited second", confirmed.data)

    def test_confirmed_questions_can_complete_a_quiz(self):
        for number in range(5):
            self.client.post(
                "/question-bank/manual",
                data={
                    "question_text": f"Question {number}",
                    "choice_a": "First",
                    "choice_b": "Second",
                    "choice_c": "Third",
                    "choice_d": "Fourth",
                    "correct_choice": "a",
                    "explanation": "First is correct.",
                },
            )
        setup = self.client.post(
            "/quiz/setup",
            data={"question_count": "5"},
            follow_redirects=True,
        )
        self.assertEqual(setup.status_code, 200)
        for _ in range(5):
            question = self.client.get("/quiz/question")
            self.assertIn(b"Submit answer", question.data)
            feedback = self.client.post(
                "/quiz/question",
                data={"selected_choice": "a"},
            )
            self.assertIn(b"The correct answer is", feedback.data)
            next_response = self.client.post("/quiz/next", follow_redirects=True)
        self.assertIn(b"5/5", next_response.data)

    def test_completed_quiz_appears_in_history_and_overview(self):
        for number in range(5):
            self.client.post(
                "/question-bank/manual",
                data={
                    "question_text": f"History question {number}",
                    "choice_a": "First",
                    "choice_b": "Second",
                    "choice_c": "Third",
                    "choice_d": "Fourth",
                    "correct_choice": "a",
                    "explanation": "First is correct.",
                },
            )
        self.client.post("/quiz/setup", data={"question_count": "5"})
        for _ in range(5):
            self.client.post("/quiz/question", data={"selected_choice": "a"})
            response = self.client.post("/quiz/next", follow_redirects=True)
        self.assertIn(b"5/5", response.data)
        history = self.client.get("/history")
        self.assertIn(b"5/5", history.data)
        detail = self.client.get("/history/1")
        self.assertIn(b"History question", detail.data)
        overview = self.client.get("/")
        self.assertIn(b"100%", overview.data)

    def test_delete_question_requires_post_and_removes_question(self):
        self.client.post(
            "/question-bank/manual",
            data={
                "question_text": "Delete me",
                "choice_a": "First",
                "choice_b": "Second",
                "choice_c": "Third",
                "choice_d": "Fourth",
                "correct_choice": "a",
                "explanation": "First is correct.",
            },
        )
        question_bank = self.client.get("/question-bank")
        self.assertIn(b"Delete me", question_bank.data)
        database_path = Path(self.temp_dir.name) / "test.sqlite3"
        import sqlite3

        connection = sqlite3.connect(database_path)
        try:
            question_id = connection.execute(
                "SELECT id FROM questions WHERE question_text = ?", ("Delete me",)
            ).fetchone()[0]
        finally:
            connection.close()
        response = self.client.post(
            f"/question-bank/{question_id}/delete",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Delete me", response.data)
        self.assertIn(b"Question deleted", response.data)

    def test_clear_database_requires_post_and_removes_questions(self):
        self.client.post(
            "/question-bank/manual",
            data={
                "question_text": "Clear me",
                "choice_a": "First",
                "choice_b": "Second",
                "choice_c": "Third",
                "choice_d": "Fourth",
                "correct_choice": "a",
                "explanation": "First is correct.",
            },
        )
        confirmation = self.client.get("/question-bank/clear")
        self.assertEqual(confirmation.status_code, 200)
        self.assertIn(b"This action cannot be undone", confirmation.data)
        self.assertIn(b"Clear me", self.client.get("/question-bank").data)
        response = self.client.post("/question-bank/clear", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Clear me", response.data)
        self.assertIn(b"Deleted 1 question", response.data)

    def test_unusable_pdf_shows_recovery_message(self):
        response = self.client.post(
            "/question-bank/import",
            data={"question_file": (BytesIO(b"not a pdf"), "broken.pdf")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"could not", response.data.lower())
        self.assertIn(b"manual", response.data.lower())


if __name__ == "__main__":
    unittest.main()
