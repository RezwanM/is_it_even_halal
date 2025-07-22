import os
import pytest

from flaskr.web_app import (
    url,
    ingredient_map_file,
    messages_file,
    messages_json,
    haram_ingredients_file,
    haram_ingredients_json,
)


@pytest.fixture
def arguments():
    test_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    languages = ["english", "bengali", "arabic"]
    return test_url, languages


def test_url(arguments):
    test_url, languages = arguments
    assert url == test_url


def test_ingredient_map_file():
    assert os.path.exists(ingredient_map_file)


def test_messages_file():
    assert os.path.exists(messages_file)


def test_haram_ingredients_file():
    assert os.path.exists(haram_ingredients_file)


def test_language_support_messages(arguments):
    test_url, languages = arguments
    assert list(messages_json.keys()) == languages


def test_language_support_haram_ingredients(arguments):
    test_url, languages = arguments
    assert list(haram_ingredients_json.keys()) == languages
