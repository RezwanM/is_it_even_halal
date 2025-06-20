import json
import os
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request, render_template
from typing import Set


app = Flask(__name__)
haram_list = set()


@app.route("/", methods=["POST", "GET"])
def index():
    load_dotenv()
    api_key = os.environ.get("USDA_API_KEY")
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    ingredients = set()
    animal_derived_ingredients = [
        "enzymes",
        "whey",
        "lard",
        "meat",
        "bacon",
        "pepperoni",
        "pork",
        "ham",
        "chicken",
        "beef",
        "lamb",
        "goat",
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
        params = {
            "query": query,
            "requireAllWords": "true",
            "dataType": ["Branded"],
            "marketCountry": "United States",
            "numberOfResultsPerPage": 1,
            "pageSize": 1,
            "api_key": api_key,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            for item in response.json()["foods"]:
                ingredients_list = item["ingredients"].split(",")
                for ingredient in ingredients_list:
                    ingredients.add(ingredient.strip().lower())
                    if ingredient.strip().lower() in haram_ingredients:
                        haram_list.add(ingredient.strip().upper())
            if haram_list:
                message = f"Showing result for category: {response.json()["foods"][0]["foodCategory"]}.\n"
                message += f"The item might not be halal as it contains:"
            elif not response.json()["foods"]:
                message = f"Information not found! Please type in full product name."
            else:
                message = f"Showing result for category: {response.json()["foods"][0]["foodCategory"]}.\n"
                message += "The item is halal."
        else:
            message = "Error! Please try again!"
        return redirect(url_for("result", message=message))
    return render_template("index.html")


@app.route("/result/<string:message>")
def result(message: str):
    formatted_message = message.replace("\n", "</br>")
    return render_template(
        "result.html", message=formatted_message, haram_list=haram_list
    )


if __name__ == "__main__":
    app.run(debug=True)
