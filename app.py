import json
import tempfile
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from db.connection import close_db, init_db
from db.queries import add_question, get_question_count, get_questions
from services.pdf_extractor import extract_pdf_text
from services.question_parser import parse_questions


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

    @app.post("/question-bank/import")
    def import_questions():
        uploaded_file = request.files.get("question_file")
        if uploaded_file is None or not uploaded_file.filename:
            flash("Choose a PDF file before importing.", "error")
            return redirect(url_for("question_bank"))
        if not uploaded_file.filename.lower().endswith(".pdf"):
            flash("For this version, choose a PDF file.", "error")
            return redirect(url_for("question_bank"))

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temporary_file:
            uploaded_file.save(temporary_file)
            temporary_path = temporary_file.name

        try:
            extracted_text = extract_pdf_text(temporary_path)
            questions = parse_questions(extracted_text)
        except (OSError, ValueError) as error:
            flash(str(error), "error")
            return redirect(url_for("question_bank"))
        finally:
            Path(temporary_path).unlink(missing_ok=True)

        session["import_preview"] = json.dumps(questions)
        session["import_source"] = secure_filename(uploaded_file.filename)
        return redirect(url_for("import_preview"))

    @app.get("/question-bank/import/preview")
    def import_preview():
        preview_data = session.get("import_preview")
        if not preview_data:
            flash("There is no import preview to review.", "error")
            return redirect(url_for("question_bank"))
        return render_template(
            "import_preview.html",
            questions=json.loads(preview_data),
            source_name=session.get("import_source", "uploaded PDF"),
        )

    @app.post("/question-bank/import/cancel")
    def cancel_import():
        session.pop("import_preview", None)
        session.pop("import_source", None)
        flash("Import cancelled. Your question bank was not changed.", "success")
        return redirect(url_for("question_bank"))

    @app.post("/question-bank/import/confirm")
    def confirm_import():
        flash(
            "Preview confirmed. Saving imported questions will be connected in the next build slice.",
            "success",
        )
        return redirect(url_for("import_preview"))

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
