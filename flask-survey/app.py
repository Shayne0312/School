from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for flashing messages


class Question:
    def __init__(self, question, choices=None, allow_text=False):
        if not choices:
            choices = ["Yes", "No"]
        self.question = question
        self.choices = choices
        self.allow_text = allow_text


class Survey:
    def __init__(self, title, instructions, questions):
        self.title = title
        self.instructions = instructions
        self.questions = questions


# Create an instance of the Survey class
satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question(
            "On average, how much do you spend a month on frisbees?",
            ["Less than $10,000", "$10,000 or more"],
        ),
        Question("Are you likely to shop here again?"),
    ],
)


@app.before_request
def initialize_session():
    session.setdefault("responses", [])


@app.route("/")
def index():
    session.clear()  # Clear session data when starting a new survey
    return render_template(
        "survey.html",
        survey_title=satisfaction_survey.title,
        instructions=satisfaction_survey.instructions,
    )


@app.route("/start_survey", methods=["POST"])
def start_survey():
    session["responses"] = []  # Set session["responses"] to an empty list
    return redirect(url_for("question", question_index=0))


@app.route("/questions/<int:question_index>", methods=["GET", "POST"])
def question(question_index):
    responses = session.get("responses")
    if len(responses) == len(satisfaction_survey.questions):
        flash("You have already answered all the questions.")
        return redirect(url_for("thank_you"))

    if question_index != len(responses):
        flash("You are trying to access an invalid question.")
        return redirect(url_for("question", question_index=len(responses)))

    if request.method == "POST":
        answer = request.form.get("answer")
        responses.append(answer)
        session["responses"] = responses  # Update the session with the new responses
        next_question_index = question_index + 1
        if next_question_index < len(satisfaction_survey.questions):
            return redirect(url_for("question", question_index=next_question_index))
        else:
            return redirect(url_for("thank_you"))

    current_question = satisfaction_survey.questions[question_index]
    return render_template(
        "question.html",
        question=current_question,
        question_index=question_index,
    )


@app.route("/finish")
def finish_survey():
    return render_template("finish.html", responses=session.get("responses"))


@app.route("/thank_you")
def thank_you():
    return render_template("survey_again.html")

@app.route("/survey_again", methods=["POST"])
def survey_again():
    survey_again = request.form.get("survey_again")
    if survey_again == "yes":
        return redirect(url_for("index"))
    elif survey_again == "no":
        return redirect(url_for("thank_you"))


if __name__ == "__main__":
    app.run()