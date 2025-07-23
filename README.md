# is_it_even_halal

The idea of this project was to create an application that could check whether a food item is considered *halal* - an Arabic word meaning *permissible*, which, in the context of food, describes items which are allowed to be consumed by Muslims according to Islamic teachings. This project uses the public API provided by the U.S. Department of Agriculture (USDA) in order to obtain the relevant information on food items requested by the user. If a food item is found in the database, and the result of the query marks the item as potentially *haram* (*impermissible* in Arabic), then the output will also list out the ingredients responsible for this labelling along with a brief explanation foreach ingredient.

The application created in this project has both a command-line version and a web version. The web version was created using Python's Flask framework.

## Preview

    $ python3 <project_root>/flaskr/cli_app.py
    Select your language ("English", "Bengali", or "Arabic"): english
    Enter item name: marshmallow
    Product:
    PEEPS - Just Born, Inc. - MARSHMALLOW
    Result:
    MIGHT NOT BE HALAL
    Reason:
    - gelatin: If this protein comes from an animal which is not halal 
    or which was not slaughtered in a halal way, then it is considered 
    haram.

## Requirements

- Python 3.12.9
- deep-translator 1.11.4
- Flask 3.1.1
- python-dotenv 1.1.0
- requests 2.32.3

## Setup
The following instructions assume the user has Ubuntu as their local machine's OS. Most instructions should work for other Linux distributions as well, though mileage may vary.

### Step 1: Install Python3
Set up Python3 (v3.12.9) on the local machine.

    sudo apt update 
    sudp apt install python3.12
    
### Step 2: Clone the project
Clone this GitHub repository into the local machine.
    
    git clone --single-branch -b main <project_repo_url> <project_root> 
    
### Step 3: Set up a virtual environment
To resolve project dependencies, install Python3 and the required packages for this project inside a virtual environment. 
    
    cd <project_root> 
    python3 -m venv .venv 
    source .venv/bin/activate
    pip install -r requirements.txt

### Step 4: Obtain the API key
Fill out the form in the link below using a personal email address. Once approved, the private API key will be sent to that email address.
https://fdc.nal.usda.gov/api-key-signup

Note: DO NOT share this API key with anyone!

### Step 5: Store the API key
Create a file inside the project root directory and store the private API key in the file.
    
    touch .env 
    echo "USDA_API_KEY=<private_api_key>" > .env

### Step 5: Run the application
Use either the command-line version or the web version of the application.

## Options

| Script             | Description                                                                         |
| ------------------ | ----------------------------------------------------------------------------------- |
| flaskr/cli_app.py  | For launching the command-line version of is_it_even_halal in an interactive shell. |
| flaskr/web_app.py  | For launching the web version of is_it_even_halal on a browser.                     |

## Usage
    
    cd <project_root>
    python3 flaskr/<cli-or-web-app-script> 
