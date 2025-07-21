import json
import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request, render_template
from typing import Dict, Set


app = Flask(__name__)

with open("messages.json", "r") as f:
    messages_json = json.load(f)

with open("haram_ingredients.json", "r") as f:
    haram_ingredients_json = json.load(f)


@app.route("/", methods=["POST", "GET"])
def base():
    if request.method == "POST":
        lang = request.form["lang"]
        if not lang:
            lang = "english"
        messages = messages_json[lang]
        return redirect(
            url_for(
                "submit",
                language=lang,
                prompt=messages["submit_prompt"],
                button=messages["submit_button"],
            )
        )
    return render_template("base.html")


@app.route("/submit/<string:language>/<string:prompt>/<string:button>", methods=["POST", "GET"])
def submit(language: str, prompt: str, button: str):
    load_dotenv()
    api_key = os.environ.get("USDA_API_KEY")
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    ingredients = set()
    haram_list = set()
    haram_ingredients = haram_ingredients_json[language].keys()
    messages = messages_json[language]
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
                        haram_list.add(ingredient.strip())
            translated_output = GoogleTranslator(source="auto", target=language).translate(text=f"{response.json()["foods"][0]["brandName"]} - {response.json()["foods"][0]["brandOwner"]} - {response.json()["foods"][0]["description"]}")
            if haram_list:
                message = f"{messages["result_success"]} {translated_output}\n"
                message += messages["result_success_haram"] 
            elif not response.json()["foods"]:
                message = messages["result_failure_search"]
            else:
                message = f"{messages["result_success"]} {translated_output}\n"
                message += messages["result_success_halal"] 
        else:
            message = messages["result_failure_webpage"]
        return redirect(
            url_for(
                "result",
                message=message,
                haram_list=haram_list,
                language=language,
            )
        )
    return render_template("submit.html",
                           language=language,
                           prompt=messages["submit_prompt"],
                           button=messages["submit_button"],
           )


@app.route("/result/<string:message>/<string:haram_list>/<string:language>")
def result(message: str, haram_list: Set[str], language: str):
    formatted_message = message.replace("\n", "<br>")
    haram_string = haram_list.lstrip("{").rstrip("}")
    stripped_list = haram_string.split(",")
    for i in range(len(stripped_list)):
        stripped_list[i] = stripped_list[i].strip(" ").strip("'").strip("set()").lower()
    return render_template(
        "result.html",
        message=formatted_message,
        haram_list=stripped_list,
        haram_dict=haram_ingredients_json[language],
    )


if __name__ == "__main__":
    app.run(debug=True)
