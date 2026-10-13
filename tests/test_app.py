import tempfile
import unittest
from pathlib import Path

from app import create_app


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


if __name__ == "__main__":
    unittest.main()
