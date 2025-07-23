import json
import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request, render_template
from typing import Dict, Set


app = Flask(__name__)

url = "https://api.nal.usda.gov/fdc/v1/foods/search"
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ingredient_map_file = os.path.join(project_root, "flaskr", "ingredient_map.json")
messages_file = os.path.join(project_root, "flaskr", "messages.json")
haram_ingredients_file = os.path.join(project_root, "flaskr", "haram_ingredients.json")
unconditionally_haram_list = ("lard", "bacon", "pork", "ham", "alcohol", "ethanol", "vanilla extract", "wine vinegar", "malt extract", "carmine", "e120")  
with open(ingredient_map_file, "r", encoding="utf-8") as f:
    ingredient_map_json = json.load(f)
with open(messages_file, "r", encoding="utf-8") as f:
    messages_json = json.load(f)
with open(haram_ingredients_file, "r", encoding="utf-8") as f:
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


@app.route(
    "/submit/<string:language>/<string:prompt>/<string:button>", methods=["POST", "GET"]
)
def submit(language: str, prompt: str, button: str):
    load_dotenv()
    api_key = os.environ.get("USDA_API_KEY")
    ingredients = set()
    haram_list = set()
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
            if not response.json()["foods"]:
                message = messages["result_failure_search"]
            else:
                for item in response.json()["foods"]:
                    ingredients_list = item["ingredients"].split(",")
                    for ingredient in ingredients_list:
                        ingredients.add(ingredient.strip().lower())
                        if ingredient.strip().lower() in haram_ingredients_json["english"]:
                            haram_list.add(ingredient.strip())
                brand_name = response.json()["foods"][0].get("brandName", "N/A")
                brand_owner = response.json()["foods"][0].get("brandOwner", "N/A")
                description = response.json()["foods"][0].get("description", "N/A")
                translated_output = GoogleTranslator(source="auto", target=language).translate(
                    text=f"{brand_name} - {brand_owner} - {description}"
                )
                message = f"{messages["result_product"]}\n"
                message += f"{translated_output}\n\n"
                message += f"{messages["result_status"]}\n"
                if haram_list:
                    unconditionally_haram = False
                    for ingredient in haram_list:
                        if ingredient in unconditionally_haram_list:
                            unconditionally_haram = True
                            break
                    if unconditionally_haram:
                        message += f"{messages["result_haram"]}\n\n"
                    else:
                        message += f"{messages["result_might"]}\n\n"
                    message += messages["result_reason"]
                else:
                    message += messages["result_halal"]
        else:
            message = messages["result_failure_webpage"]
        return redirect(
            url_for(
                "result",
                language=language,
                message=message,
                haram_list=haram_list,
                button=messages["result_button"],
            )
        )
    return render_template(
        "submit.html",
        language=language,
        prompt=messages["submit_prompt"],
        button=messages["submit_button"],
    )


@app.route(
    "/result/<string:language>/<string:message>/<string:haram_list>/<string:button>"
)
def result(language: str, message: str, haram_list: Set[str], button: str):
    formatted_message = message.replace("\n", "<br>")
    haram_string = haram_list.lstrip("{").rstrip("}")
    stripped_list = haram_string.split(",")
    for i in range(len(stripped_list)):
        stripped_list[i] = stripped_list[i].strip(" ").strip("'").strip("set()").lower()
        stripped_list[i] = (
            ingredient_map_json[language][stripped_list[i]]
            if language != "english"
            and stripped_list[i] in ingredient_map_json[language].keys()
            else stripped_list[i]
        )
    return render_template(
        "result.html",
        message=formatted_message,
        haram_list=stripped_list,
        haram_dict=haram_ingredients_json[language],
        button=button,
    )


if __name__ == "__main__":
    app.run(debug=True)
