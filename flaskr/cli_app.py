import json
import os
import requests
from dotenv import load_dotenv


url = "https://api.nal.usda.gov/fdc/v1/foods/search"
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
messages_file = os.path.join(project_root, "flaskr", "messages.json")
haram_ingredients_file = os.path.join(project_root, "flaskr", "haram_ingredients.json")


def main():
    load_dotenv()
    api_key = os.environ.get("USDA_API_KEY")
    ingredients, haram_list = set(), set()
    with open(messages_file, "r") as f:
        messages_json = json.load(f)
    with open(haram_ingredients_file, "r") as f:
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
    haram_ingredients = haram_ingredients_json[language].keys()
    query = input("Enter the item name: ")
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
        for item in response.json()["foods"]:
            ingredients_list = item["ingredients"].split(",")
            for ingredient in ingredients_list:
                ingredients.add(ingredient.strip().lower())
                if ingredient.strip().lower() in haram_ingredients:
                    haram_list.add(ingredient.strip().lower())
        output = f"{response.json()["foods"][0]["brandName"]} - {response.json()["foods"][0]["brandOwner"]} - {response.json()["foods"][0]["description"]}"
        if haram_list:
            print(f"{messages["result_success"]} {output}")
            print(messages["result_success_haram"])
            for ingredient in haram_list:
                print(f"- {ingredient}: {haram_ingredients_json[language][ingredient]}")
        elif not response.json()["foods"]:
            print(messages["result_failure_search"])
        else:
            print(f"{messages["result_success"]} {output}")
            print(messages["result_success_halal"])
    else:
        print(f"Failed to search. Status code: {response.status_code}")


if __name__ == "__main__":
    main()
