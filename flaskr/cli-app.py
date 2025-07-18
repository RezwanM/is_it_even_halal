import json
import os
import requests
from dotenv import load_dotenv


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
    if haram_list:
        print(
            f"Showing results for: {response.json()["foods"][0]["brandName"]} - {response.json()["foods"][0]["brandOwner"]} - {response.json()["foods"][0]["description"]}"
        )
        print("This item might not be halal as it contains:")
        print(haram_list)
    elif not response.json()["foods"]:
        print("Information not found! Please type in full product name.")
    else:
        print(
            f"Showing results for: {response.json()["foods"][0]["brandName"]} - {response.json()["foods"][0]["brandOwner"]} - {response.json()["foods"][0]["description"]}"
        )
        print("This item is halal.")

else:
    print(f"Failed to search. Status code: {response.status_code}")
