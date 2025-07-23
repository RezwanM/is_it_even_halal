import json
import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv


url = "https://api.nal.usda.gov/fdc/v1/foods/search"
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ingredient_map_file = os.path.join(project_root, "flaskr", "ingredient_map.json")
messages_file = os.path.join(project_root, "flaskr", "messages.json")
haram_ingredients_file = os.path.join(project_root, "flaskr", "haram_ingredients.json")
unconditionally_haram_list = ("lard", "bacon", "pork", "ham", "alcohol", "beer", "ethanol", "vanilla extract", "wine vinegar", "malt extract", "carmine", "e120")  


def main():
    load_dotenv()
    api_key = os.environ.get("USDA_API_KEY")
    ingredients, haram_list = set(), set()
    with open(ingredient_map_file, "r", encoding="utf-8") as f:
        ingredient_map_json = json.load(f)
    with open(messages_file, "r", encoding="utf-8") as f:
        messages_json = json.load(f)
    with open(haram_ingredients_file, "r", encoding="utf-8") as f:
        haram_ingredients_json = json.load(f)
    language = input('Select your language ("English", "Bengali", or "Arabic"): ')
    lang_list = ("english", "bengali", "arabic")
    if not language:
        language = "english"
    else:
        language = language.split()[0]
        while language.lower() not in lang_list:
            language = input(
                'Invalid selection! Please type either "English", "Bengali", or "Arabic"): '
            )
        language = language.lower()
    messages = messages_json[language]
    query = input("Enter item name: ")
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
        with open("result.json", "a", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4)
        if not response.json()["foods"]:
            print(messages["result_failure_search"])
        else:
            for item in response.json()["foods"]:
                ingredients_list = item["ingredients"].split(",")
                for ingredient in ingredients_list:
                    ingredients.add(ingredient.strip().lower())
                    if ingredient.strip().lower() in haram_ingredients_json["english"]:
                        haram_list.add(ingredient.strip().lower())
            brand_name = response.json()["foods"][0].get("brandName", "N/A")
            brand_owner = response.json()["foods"][0].get("brandOwner", "N/A")
            description = response.json()["foods"][0].get("description", "N/A")
            translated_output = GoogleTranslator(source="auto", target=language).translate(
                text=f"{brand_name} - {brand_owner} - {description}"
            )
            description_list = description.split()
            for word in description_list:
                word = word.rstrip(",")
                for word in description_list:
                    word = word.rstrip(",").lower()
                    if word in haram_ingredients_json["english"]:
                        haram_list.add(word) 
            print(messages["result_product"])
            print(translated_output)
            print(messages["result_status"])
            if haram_list:
                unconditionally_haram = False
                for ingredient in haram_list:
                    if ingredient in unconditionally_haram_list:
                        unconditionally_haram = True
                        break
                if unconditionally_haram:
                    print(messages["result_haram"])
                else:
                    print(messages["result_might"])
                print(messages["result_reason"])
                for ingredient in haram_list:
                    ingredient = (
                        ingredient_map_json[language][ingredient]
                        if language != "english"
                        else ingredient
                    )
                    print(f"- {ingredient.upper()}: {haram_ingredients_json[language][ingredient]}")
            else:
                print(messages["result_halal"])
    else:
        print(f"Failed to search. Status code: {response.status_code}")


if __name__ == "__main__":
    main()
