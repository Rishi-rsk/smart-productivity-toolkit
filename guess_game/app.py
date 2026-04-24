from flask import Flask, render_template, request, session, redirect
from game_logic import Game

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/", methods=["GET", "POST"])
def index():
    if "game" not in session:
        session["game"] = Game().__dict__

    game = Game()
    game.__dict__ = session["game"]

    message = ""

    if request.method == "POST":
        guess = int(request.form["guess"])
        result = game.guess(guess)

        if result == "low":
            message = "Too low! ↑"
        elif result == "high":
            message = "Too high! ↓"
        else:
            session.pop("game", None)
            return render_template("result.html", attempts=game.attempts)

        session["game"] = game.__dict__

    return render_template("index.html", game=game, message=message)

@app.route("/reset")
def reset():
    session.pop("game", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)