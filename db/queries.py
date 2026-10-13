from collections.abc import Sequence

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
        "SELECT * FROM questions ORDER BY created_at DESC, id DESC"
    ).fetchall()
    return [dict(row) for row in rows]


def get_question_count() -> int:
    row = get_db().execute("SELECT COUNT(*) AS count FROM questions").fetchone()
    return int(row["count"])
