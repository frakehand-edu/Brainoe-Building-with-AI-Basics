from collections.abc import Sequence
from datetime import datetime

from db.connection import get_db


def add_question(
    question_text: str,
    choices: Sequence[str],
    correct_choice: str,
    explanation: str,
    source_name: str,
) -> int:
    if len(choices) != 4:
        raise ValueError("A question must have exactly four choices.")

    database = get_db()
    cursor = database.execute(
        """
        INSERT INTO questions (
            question_text, choice_a, choice_b, choice_c, choice_d,
            correct_choice, explanation, source_name
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            question_text,
            choices[0],
            choices[1],
            choices[2],
            choices[3],
            correct_choice,
            explanation,
            source_name,
        ),
    )
    database.commit()
    return int(cursor.lastrowid)


def get_questions() -> list[dict]:
    rows = get_db().execute(
        "SELECT * FROM questions ORDER BY created_at ASC, id ASC"
    ).fetchall()
    return [dict(row) for row in rows]


def get_question_count() -> int:
    row = get_db().execute("SELECT COUNT(*) AS count FROM questions").fetchone()
    return int(row["count"])


def delete_question(question_id: int) -> bool:
    database = get_db()
    cursor = database.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    database.commit()
    return cursor.rowcount == 1


def clear_questions() -> int:
    database = get_db()
    cursor = database.execute("DELETE FROM questions")
    database.commit()
    return cursor.rowcount


def add_questions(questions: list[dict], source_name: str) -> int:
    database = get_db()
    database.executemany(
        """
        INSERT INTO questions (
            question_text, choice_a, choice_b, choice_c, choice_d,
            correct_choice, explanation, source_name
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                question["question_text"],
                question["choices"][0],
                question["choices"][1],
                question["choices"][2],
                question["choices"][3],
                question["correct_choice"],
                question["explanation"],
                source_name,
            )
            for question in questions
        ],
    )
    database.commit()
    return len(questions)


def get_questions_by_ids(question_ids: Sequence[int]) -> list[dict]:
    if not question_ids:
        return []
    placeholders = ",".join("?" for _ in question_ids)
    rows = get_db().execute(
        f"SELECT * FROM questions WHERE id IN ({placeholders})",
        list(question_ids),
    ).fetchall()
    by_id = {int(row["id"]): dict(row) for row in rows}
    return [by_id[int(question_id)] for question_id in question_ids if int(question_id) in by_id]


def save_attempt(question_ids: Sequence[int], answers: Sequence[str]) -> int:
    questions = get_questions_by_ids(question_ids)
    if len(questions) != len(answers) or not questions:
        raise ValueError("Quiz answers do not match the selected questions.")

    correct_count = sum(
        answer == question["correct_choice"]
        for question, answer in zip(questions, answers)
    )
    question_count = len(questions)
    percentage = round(correct_count / question_count * 100, 1)
    database = get_db()
    cursor = database.execute(
        """
        INSERT INTO quiz_attempts (question_count, correct_count, percentage, started_at, completed_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            question_count,
            correct_count,
            percentage,
            datetime.now().isoformat(timespec="seconds"),
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    attempt_id = int(cursor.lastrowid)
    database.executemany(
        """
        INSERT INTO attempt_questions (
            attempt_id, question_id, question_order, selected_choice, is_correct
        ) VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                attempt_id,
                question["id"],
                index,
                answer,
                answer == question["correct_choice"],
            )
            for index, (question, answer) in enumerate(zip(questions, answers), start=1)
        ],
    )
    database.commit()
    return attempt_id


def get_attempt(attempt_id: int) -> dict | None:
    row = get_db().execute(
        "SELECT * FROM quiz_attempts WHERE id = ?", (attempt_id,)
    ).fetchone()
    return dict(row) if row else None


def get_attempts() -> list[dict]:
    rows = get_db().execute(
        "SELECT * FROM quiz_attempts ORDER BY completed_at DESC, id DESC"
    ).fetchall()
    return [dict(row) for row in rows]


def get_attempt_review(attempt_id: int) -> list[dict]:
    rows = get_db().execute(
        """
        SELECT aq.question_order, aq.selected_choice, aq.is_correct,
               q.question_text, q.choice_a, q.choice_b, q.choice_c, q.choice_d,
               q.correct_choice, q.explanation
        FROM attempt_questions AS aq
        JOIN questions AS q ON q.id = aq.question_id
        WHERE aq.attempt_id = ?
        ORDER BY aq.question_order
        """,
        (attempt_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def get_progress_stats() -> dict:
    attempts = get_attempts()
    if not attempts:
        return {
            "streak": 0,
            "daily_accuracy": None,
            "weekly_accuracy": None,
            "practice_days": set(),
        }

    today = datetime.now().date()
    practice_days = {
        datetime.fromisoformat(attempt["completed_at"]).date()
        for attempt in attempts
    }
    streak = 0
    cursor = today
    while cursor in practice_days:
        streak += 1
        cursor = cursor.fromordinal(cursor.toordinal() - 1)

    daily_attempts = [
        attempt
        for attempt in attempts
        if datetime.fromisoformat(attempt["completed_at"]).date() == today
    ]
    weekly_attempts = [
        attempt
        for attempt in attempts
        if (today - datetime.fromisoformat(attempt["completed_at"]).date()).days < 7
    ]

    def accuracy(items: list[dict]) -> float | None:
        total = sum(item["question_count"] for item in items)
        correct = sum(item["correct_count"] for item in items)
        return round(correct / total * 100) if total else None

    return {
        "streak": streak,
        "daily_accuracy": accuracy(daily_attempts),
        "weekly_accuracy": accuracy(weekly_attempts),
        "practice_days": practice_days,
    }
