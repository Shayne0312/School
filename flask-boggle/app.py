from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
boggle_game = Boggle()

@app.route("/")
def homepage():
    """
    Show the Boggle board.
    """
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)

@app.route("/check-word")
def check_word():
    """
    Check if a word is in the dictionary and on the Boggle board.
    """
    word = request.args["word"].lower()
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    print(response)
    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """
    Receive the score, update the number of plays (nplays),
    and update the high score if appropriate.
    """
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    return jsonify(brokeRecord=score > highscore)