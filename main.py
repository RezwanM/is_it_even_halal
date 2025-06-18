import json
import os
import requests
from dotenv import load_dotenv 


load_dotenv()
api_key=os.environ.get("USDA_API_KEY")
url = "https://api.nal.usda.gov/fdc/v1/foods/search"
ingredients = set() 
haram_list = set() 
animal_derived_ingredients = ["enzymes", "whey", "lard", "bacon", "ham", "gelatin", "rennet", "l-cysteine", "pepsin"]
alcohol_ingredients = ["alcohol", "ethanol", "vanilla extract", "wine vinegar", "malt extract"] 
additives_ingredients = ["monoglycerides", "diglycerides", "glycerin", "glycerol", "shortening", "magensium stearate"]  
insects_derived_ingredients = ["carmine (e120)"]
haram_ingredients = animal_derived_ingredients + alcohol_ingredients + additives_ingredients + insects_derived_ingredients 
query = input("Enter the item name: ")
params = {
    "query": query,
    "dataType": ["Branded"],
    "api_key": api_key
}
response = requests.get(url, params=params)
if response.status_code == 200:
    with open("result.json", "a", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=4)
    for item in response.json()["foods"]:
        ingredients_list = item["ingredients"].split(',')
        for ingredient in ingredients_list:
            ingredients.add(ingredient.strip().lower())
            if ingredient.strip().lower() in haram_ingredients:
                haram_list.add(ingredient.strip().lower())
    if haram_list:
        print("This item might not be halal as it contains:") 
        print(haram_list)
    else:
        print("This item is halal.")

else:
    print(f"Failed to search. Status code: {response.status_code}")
