import json
import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request, render_template
from typing import Set

from haram_info import Info


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def base():
    load_dotenv()
    api_key = os.environ.get("USDA_API_KEY")
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    ingredients = set()
    haram_list = set()
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
        "e471",
        "glycerin",
        "glycerol",
        "e422",
        "shortening",
        "magensium stearate",
    ]
    insects_derived_ingredients = [
        "carmine",
        "e120",
    ]
    haram_ingredients = (
        animal_derived_ingredients
        + alcohol_ingredients
        + additives_ingredients
        + insects_derived_ingredients
    )
    if request.method == "POST":
        lang = request.form["lang"]
        if not lang:
            lang = "english"
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
                        haram_list.add(ingredient.strip())
            if haram_list:
                message = f"Showing result for: {response.json()["foods"][0]["brandName"]} - {response.json()["foods"][0]["brandOwner"]} - {response.json()["foods"][0]["description"]}\n"
                message += f"The item might not be halal as it contains:"
            elif not response.json()["foods"]:
                message = f"Information not found! Please type in full product name."
            else:
                message = f"Showing result for: {response.json()["foods"][0]["brandName"]} - {response.json()["foods"][0]["brandOwner"]} - {response.json()["foods"][0]["description"]}\n"
                message += "The item is halal."
        else:
            message = "Error! Please try again!"
        return redirect(url_for("result", message=GoogleTranslator(source='auto', target=lang).translate(text=message), haram_list=haram_list, language=lang))
    return render_template("base.html")


@app.route("/result/<string:message>/<string:haram_list>/<string:language>")
def result(message: str, haram_list: Set[str], language: str):
    translated_list = []
    formatted_message = message.replace("\n", "<br>")
    haram_string = haram_list.lstrip("{").rstrip("}")
    stripped_list = haram_string.split(",")
    for i in range(len(stripped_list)):
        stripped_list[i] = stripped_list[i].strip(" ").strip("'").strip("set()").lower()
        translated_list.append(GoogleTranslator(source='auto', target=language).translate(text=stripped_list[i]))
    return render_template(
        "result.html",
        message=formatted_message,
        haram_list=translated_list,
        haram_dict=Info().get_info(haram_list=stripped_list, language=language),
    )


if __name__ == "__main__":
    app.run(debug=True)
