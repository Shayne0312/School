from flask import Flask, render_template, request, jsonify
import random
import requests

app = Flask(__name__)

@app.route("/api/get-lucky-num", methods=["POST"])
def get_lucky_num():
    data = request.json
    errors = {}
    # Validate input
    if not data.get("name"):
        errors["name"] = ["This field is required."]
    if not data.get("email"):
        errors["email"] = ["This field is required."]
    if "year" not in data or not (1900 <= int(data["year"]) <= 2000):
        errors["year"] = ["Invalid year, must be between 1900 and 2000."]
    if data.get("color") not in ["red", "green", "orange", "blue"]:
        errors["color"] = ["Invalid value, must be one of: red, green, orange, blue."]
    
    if errors:
        return jsonify(errors=errors), 400
    
    # Generate random number and get facts
    lucky_number = random.randint(1, 100)
    num_fact = requests.get(f"http://numbersapi.com/{lucky_number}").text
    year_fact = requests.get(f"http://numbersapi.com/{data['year']}/year").text
    
    return jsonify(num={"fact": num_fact, "num": lucky_number},
                   year={"fact": year_fact, "year": data["year"]})

# The homepage route
@app.route("/")
def homepage():
    """Show homepage."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)