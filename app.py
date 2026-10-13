from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from db.connection import close_db, init_db
from db.queries import add_question, get_question_count, get_questions


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "local-development-key"
    app.config["DATABASE"] = Path(app.instance_path) / "exam_to_quiz.sqlite3"
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    with app.app_context():
        init_db(app.config["DATABASE"])

    app.teardown_appcontext(close_db)

    @app.get("/")
    def overview():
        return render_template("overview.html", question_count=get_question_count())

    @app.get("/quiz")
    def quiz_me():
        if get_question_count() < 5:
            flash(
                "You need at least 5 questions before starting a quiz. Add more questions to your Question Bank.",
                "error",
            )
            return redirect(url_for("question_bank"))
        return redirect(url_for("quiz_setup"))

    @app.get("/quiz/setup")
    def quiz_setup():
        return render_template("quiz_setup.html", question_count=get_question_count())

    @app.get("/question-bank")
    def question_bank():
        return render_template(
            "question_bank.html",
            questions=get_questions(),
            question_count=get_question_count(),
        )

    @app.route("/question-bank/manual", methods=["GET", "POST"])
    def manual_question():
        if request.method == "POST":
            question_text = request.form.get("question_text", "").strip()
            choices = [request.form.get(f"choice_{letter}", "").strip() for letter in "abcd"]
            correct_choice = request.form.get("correct_choice", "").strip().lower()
            explanation = request.form.get("explanation", "").strip()

            if not question_text or any(not choice for choice in choices):
                flash("Add a question and all four answer choices.", "error")
            elif correct_choice not in "abcd":
                flash("Choose the correct answer before saving.", "error")
            elif not explanation:
                flash("Add a short explanation so feedback is useful.", "error")
            else:
                add_question(
                    question_text=question_text,
                    choices=choices,
                    correct_choice=correct_choice,
                    explanation=explanation,
                    source_name="manual",
                )
                flash("Question added to your question bank.", "success")
                return redirect(url_for("question_bank"))

        return render_template("manual_question.html")

    @app.get("/history")
    def history():
        return render_template("history.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
