#! /usr/bin/env python3
import textwrap
import requests


def show_title():
    """
        This method displays the title to screen
    """
    print("My Recipes Program")
    print()


def show_menu():
    """
        This method displays the menu to screen
    """
    print("COMMAND MENU")
    print("1 - List all Categories")
    print("2 - List all Meals for a Category")
    print("3 - Search Meal by Name")
    print("4 - Random Meal")
    print("5 - List all Areas")
    print("6 - Search Meals by Area")
    print("7 - Menu")
    print("0 - Exit the program")
    print()


def list_categories(categories):
    """
        This method displays the list of categories to screen
    """
    print("CATEGORIES")
    for i in range(len(categories)):
        category = categories[i]
        print(category.get_category())
    print()


def list_meals_by_category(category, meals):
    """
        This method displays the list of meals to screen
    """
    print()
    print(category.upper() + " MEALS")
    for i in range(len(meals)):
        meal = meals[i]
        print(meal.get_meal())
    print()


def search_meal_by_category(categories):
    """
        This method is used to get a category to search for meals on
        and then make the call to get the list of meals for the category
    """

    lookup_category = input("Enter a Category: ")
    found = False

    # validate categories
    for i in range(len(categories)):
        category = categories[i]
        if category.get_category().lower() == lookup_category.lower():
            found = True
            break

    if found:
        meals = requests.get_meals_by_category(lookup_category)
        list_meals_by_category(lookup_category, meals)
    else:
        print("Invalid Category, please try again")
        print()


def list_areas(areas):
    """
        This method displays the list of categories to screen
    """
    print("AREAS")
    for i in range(len(areas)):
        area = areas[i]
        print(area.get_area())
    print()


def list_meals_by_area(area, meals):
    """
        This method displays the list of meals to screen
    """
    print()
    print(area.upper() + " MEALS")
    for i in range(len(meals)):
        meal = meals[i]
        print(meal.get_meal())
    print()


def search_meal_by_area(areas):
    """
        This method is used to get an area to search for meals on
        and then make the call to get the list of meals for the area
    """

    lookup_area = input("Enter an Area: ")
    found = False

    # validate categories
    for i in range(len(areas)):
        area = areas[i]
        if area.get_area().lower() == lookup_area.lower():
            found = True
            break

    if found:
        meals = requests.get_meals_by_area(lookup_area.title())
        list_meals_by_area(lookup_area, meals)
    else:
        print("Invalid Area, please try again")
        print()


def display_recipe(recipe):
    """
        This method is used to display the meal information to screen
    """
    print()
    print("Recipe:", recipe.get_meal())
    print()
    my_wrap = textwrap.TextWrapper(width=80)
    wrap_list = my_wrap.wrap("Instructions: " + recipe.get_instructions())
    for line in wrap_list:
        print(line)
    print()


def display_ingredients(lookup_meal):

    ingredients = requests.get_ingredients_and_measurements(lookup_meal)
    formating = "{:<30}"
    print("Ingredients:")
    print("-" * 90)

    items = []      # 2-D list of all the ingredients/measurements
    count = 0
    row = []        # one row of items (holds 3 ingredients)

    for i in range(len(ingredients)):
        ingredient = ingredients[i]
        item = formating.format(ingredient.get_measure() + " " + ingredient.get_ingredient())

        if count >= 3:              # if row is full will add row to the items list
            items.append(row)
            row = []
            count = 0

        row.append(item)            # adds ingredient to row and increments counts
        count += 1

    items.append(row)

    # displays all the ingredients
    for row in items:
        for item in row:
            print(item, end=" ")
        print()
    print()


def search_meal_by_name():
    """
        This method is used to get a meal's name from the user and
        make the call to get the meal from the site
    """
    lookup_meal = input("Enter Meal Name: ")

    meal = requests.get_meal_by_name(lookup_meal)
    if meal:
        display_recipe(meal)
        display_ingredients(lookup_meal)
    else:
        print("A recipe for this meal was not found.")
        print()


def display_random_recipe():
    """
        This method is used to get a random meal and display its
        recipe and ingredients
    """
    random_name = requests.get_random_meal()
    random_meal = requests.get_meal_by_name(random_name)
    display_recipe(random_meal)
    display_ingredients(random_name)


def main():
    """
        This method controls the flow of the program
    """

    # Show the title and menu to screen
    show_title()
    show_menu()

    # Get the list of categories
    categories = requests.get_categories()

    # Get the list of areas
    areas = requests.get_areas()

    # Get the user menu selection
    while True:
        command = input("Command: ")

        if command == "1":
            list_categories(categories)
        elif command == "2":
            search_meal_by_category(categories)
        elif command == "3":
            search_meal_by_name()
        elif command == "4":
            print("A random meal was selected just for you!")
            display_random_recipe()
        elif command == "5":
            list_areas(areas)
        elif command == "6":
            search_meal_by_area(areas)
        elif command == "7":
            show_menu()
        elif command == "0":
            print("Thank you for dining with us!")
            break
        else:
            print("Not a valid command. Please try again.\n")


if __name__ == "__main__":
    main()