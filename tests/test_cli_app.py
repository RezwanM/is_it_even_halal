import os
import pytest

from flaskr.cli_app import (
    url,
    ingredient_map_file,
    messages_file,
    haram_ingredients_file,
)


@pytest.fixture
def arguments():
    test_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    return test_url


def test_url(arguments):
    test_url = arguments
    assert url == test_url


def test_ingredient_map_file():
    assert os.path.exists(ingredient_map_file)


def test_messages_file():
    assert os.path.exists(messages_file)


def test_haram_ingredients_file():
    assert os.path.exists(haram_ingredients_file)
