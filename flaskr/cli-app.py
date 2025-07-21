import json
import os
import requests
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get("USDA_API_KEY")
url = "https://api.nal.usda.gov/fdc/v1/foods/search"
ingredients = set()
haram_list = set()
with open("messages.json", "r") as f:
    messages_json = json.load(f)
messages = messages_json["english"]
with open("haram_ingredients.json", "r") as f:
    haram_ingredients_json = json.load(f)
haram_ingredients = haram_ingredients_json["english"].keys()
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
            print(ingredient)
    elif not response.json()["foods"]:
        print(messages["result_failure_search"])
    else:
        print(f"{messages["result_success"]} {output}")
        print(messages["result_success_halal"])
else:
    print(f"Failed to search. Status code: {response.status_code}")
