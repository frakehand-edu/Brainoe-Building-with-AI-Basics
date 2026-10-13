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
        app.config.update(
            TESTING=True,
            DATABASE=Path(self.temp_dir.name) / "test.sqlite3",
        )
        from db.connection import init_db

        init_db(app.config["DATABASE"])
        self.client = app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_main_pages_load(self):
        for path in ("/", "/question-bank", "/history", "/question-bank/manual"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)

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


if __name__ == "__main__":
    unittest.main()
