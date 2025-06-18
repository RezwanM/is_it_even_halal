import json
import os
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def check_halal():
    load_dotenv()
    api_key = os.environ.get("USDA_API_KEY")
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    ingredients = set()
    haram_list = set()
    animal_derived_ingredients = [
        "enzymes",
        "whey",
        "lard",
        "bacon",
        "ham",
        "gelatin",
        "rennet",
        "l-cysteine",
        "pepsin",
    ]
    alcohol_ingredients = [
        "alcohol",
        "ethanol",
        "vanilla extract",
        "wine vinegar",
        "malt extract",
    ]
    additives_ingredients = [
        "monoglycerides",
        "diglycerides",
        "glycerin",
        "glycerol",
        "shortening",
        "magensium stearate",
    ]
    insects_derived_ingredients = ["carmine (e120)"]
    haram_ingredients = (
        animal_derived_ingredients
        + alcohol_ingredients
        + additives_ingredients
        + insects_derived_ingredients
    )
    if request.method == "POST":
        query = request.form["nm"]
    else:
        query = request.args.get("nm")
    params = {"query": query, "dataType": ["Branded"], "api_key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        for item in response.json()["foods"]:
            ingredients_list = item["ingredients"].split(",")
            for ingredient in ingredients_list:
                ingredients.add(ingredient.strip().lower())
                if ingredient.strip().lower() in haram_ingredients:
                    haram_list.add(ingredient.strip().lower())
        if haram_list:
            message = f"This item might not be halal as it contains: {haram_list}"
            return redirect(url_for("result", message=message))
        else:
            message = "This item is halal."
            return redirect(url_for("result", message=message))
    else:
        message = "Error! Please try again!"
        return redirect(url_for("result", message=message))


@app.route("/result/<string:message>")
def result(message: str):
    return "%s" % message


if __name__ == "__main__":
    app.run(debug=True)
