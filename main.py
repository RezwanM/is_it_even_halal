import os
from dotenv import load_dotenv 


load_dotenv()

api_key=os.environ.get("USDA_API_KEY")

print(api_key)

