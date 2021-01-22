#! /usr/bin/env python3
from urllib import request, parse
import json

from objects import Category, Meal, Recipe, Ingredient, Area


# Get a list of the meal categories
def get_categories():
    url = 'https://www.themealdb.com/api/json/v1/1/list.php?c=list'
    f = request.urlopen(url)
    categories = []

    try:
        data = json.loads(f.read().decode('utf-8'))
        for category_data in data['meals']:
            category = Category(category_data['strCategory'])

            categories.append(category)
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

    return categories


# List all meals by Category
def get_meals_by_category(category):
    url = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=' + category
    f = request.urlopen(url)
    meals = []

    try:
        data = json.loads(f.read().decode('utf-8'))
        for meal_data in data['meals']:
            category = Meal(meal_data['idMeal'],
                            meal_data['strMeal'],
                            meal_data['strMealThumb'])
            meals.append(category)
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

    return meals


# Get a list of areas
def get_areas():
    url = 'https://www.themealdb.com/api/json/v1/1/list.php?a=list'
    f = request.urlopen(url)
    areas = []

    try:
        data = json.loads(f.read().decode('utf-8'))
        for area_data in data['meals']:
            area = Area(area_data['strArea'])

            areas.append(area)
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

    return areas


# List all meals by Area
def get_meals_by_area(area):
    url = 'https://www.themealdb.com/api/json/v1/1/filter.php?a=' + area
    f = request.urlopen(url)
    meals = []

    try:
        data = json.loads(f.read().decode('utf-8'))
        for meal_data in data['meals']:
            area = Meal(meal_data['idMeal'],
                        meal_data['strMeal'],
                        meal_data['strMealThumb'])
            meals.append(area)
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

    return meals


# Search a Meal by Name
def get_meal_by_name(meal):
    url = 'https://www.themealdb.com/api/json/v1/1/search.php?s=' + parse.quote(meal)
    f = request.urlopen(url)

    recipe = None
    try:
        data = json.loads(f.read().decode('utf-8'))

        for recipe_data in data['meals']:
            recipe = Recipe(recipe_data['idMeal'],
                            recipe_data['strMeal'],
                            recipe_data['strCategory'],
                            recipe_data['strInstructions'],
                            recipe_data['strMealThumb'])

    except(ValueError, KeyError, TypeError):
        print("JSON format error")

    return recipe


def get_ingredients_and_measurements(lookup_meal):
    url = 'https://www.themealdb.com/api/json/v1/1/search.php?s=' + parse.quote(lookup_meal)
    f = request.urlopen(url)
    ingredients = []
    done = False

    try:
        data = json.loads(f.read().decode('utf-8'))

        for i in range(1, 20):
            ingredient_key = 'strIngredient' + str(i)
            measure_key = 'strMeasure' + str(i)

            for ingredient_data in data['meals']:

                # creates an ingredient object to store into a list
                ingredient = Ingredient(ingredient_data[ingredient_key],
                                        ingredient_data[measure_key])

                # stops loop if the ingredient is blank
                if ingredient.get_ingredient() == '':
                    done = True
                else:
                    ingredients.append(ingredient)

            # exits loop if the rest of the 20 ingredients will be blank
            if done:
                break

    except(ValueError, KeyError, TypeError):
        print("JSON format error\n")

    return ingredients


# Gets the name of the random meal
def get_random_meal():
    url = 'https://www.themealdb.com/api/json/v1/1/random.php'
    f = request.urlopen(url)

    random_name = None
    try:
        data = json.loads(f.read().decode('utf-8'))

        for recipe_data in data['meals']:
            random_name = recipe_data['strMeal']

    except(ValueError, KeyError, TypeError):
        print("JSON format error")

    return random_name
