from flask import Flask, render_template, request
import requests
from rag_engine import parse_query

app = Flask(__name__)

API_URL = "https://api.exchangerate-api.com/v4/latest/{}"

def convert_currency(amount, from_curr, to_curr):
    try:
        response = requests.get(API_URL.format(from_curr))
        data = response.json()

        rate = data["rates"][to_curr]
        return round(amount * rate, 2)
    except:
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    message = ""

    if request.method == "POST":
        user_input = request.form["query"]

        parsed = parse_query(user_input)

        if parsed:
            amount, from_curr, to_curr = parsed
            result = convert_currency(amount, from_curr, to_curr)

            if result:
                message = f"{amount} {from_curr} = {result} {to_curr}"
            else:
                message = "Conversion failed ❌"
        else:
            message = "Invalid query format ❌"

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)