import re


QUESTION_START = re.compile(r"^\s*(?:Question\s*)?(\d+)[.)]\s*(.+)$", re.IGNORECASE)
CHOICE = re.compile(r"^\s*([A-Da-d])[.)]\s*(.+)$")
ANSWER = re.compile(r"^\s*(?:Answer|Correct answer)\s*:\s*([A-Da-d])\s*$", re.IGNORECASE)
EXPLANATION = re.compile(r"^\s*Explanation\s*:\s*(.+)$", re.IGNORECASE)


def parse_questions(text: str) -> list[dict]:
    """Parse the deliberately small, documented exam-text format."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    questions: list[dict] = []
    current: dict | None = None
    explanation_lines: list[str] = []

    def finish_question() -> None:
        nonlocal current, explanation_lines
        if current is None:
            return
        if len(current["choices"]) != 4:
            current = None
            explanation_lines = []
            return
        if not current.get("correct_choice") or not explanation_lines:
            current = None
            explanation_lines = []
            return
        current["explanation"] = " ".join(explanation_lines).strip()
        current["choices"] = [current["choices"][letter] for letter in "abcd"]
        questions.append(current)
        current = None
        explanation_lines = []

    for line in lines:
        question_match = QUESTION_START.match(line)
        if question_match:
            finish_question()
            current = {
                "question_text": question_match.group(2).strip(),
                "choices": {},
                "correct_choice": "",
                "explanation": "",
            }
            continue

        if current is None:
            continue

        choice_match = CHOICE.match(line)
        if choice_match:
            current["choices"][choice_match.group(1).lower()] = choice_match.group(2).strip()
            continue

        answer_match = ANSWER.match(line)
        if answer_match:
            current["correct_choice"] = answer_match.group(1).lower()
            continue

        explanation_match = EXPLANATION.match(line)
        if explanation_match:
            explanation_lines.append(explanation_match.group(1).strip())
            continue

        if explanation_lines:
            explanation_lines.append(line)

    finish_question()
    if not questions:
        raise ValueError(
            "No usable four-choice questions were found. Use the supported format or add a question manually."
        )
    return questions
