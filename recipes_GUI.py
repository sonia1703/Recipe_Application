"""
    In order to not inadvertently overwrite or change any functions in the console application
    in recipes.py, this file, recipes_GUI.py, is completely separate from the console application
    but uses the similar functions and imports the same files and objects to display the same
    functionality just with a different GUI display.
"""

import tkinter as tk
from tkinter import ttk
import requests
import textwrap


def get_categories():
    # Get the list of categories
    categories = requests.get_categories()
    return categories


def get_areas():
    # Get the list of areas
    areas = requests.get_areas()
    return areas


def get_meal_str_c(meals_list, category_str):
    """
        This method searches for the entered category and if found will return
        a string with all the meals in that category. If not found, will return
        a string with an appropriate message.
    """

    found = False
    categories = get_categories()

    # validate categories
    for i in range(len(categories)):
        category = categories[i]
        if category.get_category().lower() == category_str.lower():
            found = True
            break

    if found:
        meals = requests.get_meals_by_category(category_str.lower())
        meals_list += category_str.upper() + " MEALS" + "\n\n"
        for i in range(len(meals)):
            meal = meals[i]
            meals_list += meal.get_meal() + "\n"
    else:
        meals_list = "Invalid Category, please try again"

    return meals_list


def get_meal_str_a(meals_list, area_str):
    """
        This method searches for the entered area and if found will return
        a string with all the meals in that area. If not found, will return
        a string with an appropriate message.
    """

    found = False
    areas = get_areas()

    # validate categories
    for i in range(len(areas)):
        area = areas[i]
        if area.get_area().lower() == area_str.lower():
            found = True
            break

    if found:
        meals = requests.get_meals_by_area(area_str.title())
        meals_list += area_str.upper() + " MEALS" + "\n\n"
        for i in range(len(meals)):
            meal = meals[i]
            meals_list += meal.get_meal() + "\n"
    else:
        meals_list = "Invalid Area, please try again"

    return meals_list


def get_recipe_str(recipe, meal_str):
    """
        This method searches for the recipe of the entered meal. If found, will
        return a string with the meal's recipe and ingredients already formatted.
        If not found, will return a string with the appropriate message
    """

    recipe_object = requests.get_meal_by_name(meal_str)
    if recipe_object:
        recipe += "Recipe: " + recipe_object.get_meal() + "\n\n"
        my_wrap = textwrap.TextWrapper(width=80)

        # Get and format the instructions
        wrap_list = my_wrap.wrap("Instructions: " + recipe_object.get_instructions())
        for line in wrap_list:
            recipe += line + "\n"

        # Get and format the ingredient/measurements
        ingredients = requests.get_ingredients_and_measurements(meal_str)
        formatting = "{:<30}"
        recipe += "\n\nIngredients:\n"
        recipe += "-" * 80 + "\n"

        try:
            for i in range(len(ingredients)):
                ingredient = ingredients[i]
                item = formatting.format(ingredient.get_measure() + " " + ingredient.get_ingredient())
                recipe += item + "\n"
        except TypeError:
            recipe = "Error in ingredient format. Try another recipe."

    else:
        recipe = "A recipe for this meal was not found."

    return recipe


class RecipeFrame(ttk.Frame):
    def __init__(self, parent):

        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)

        # Create vertical scrollbar and add to frame
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.configure_frame)

        self.pack(fill="x")
        self.parent = parent

        # Define string variables
        self.display = tk.StringVar()
        self.category = tk.StringVar()
        self.meal_name = tk.StringVar()
        self.area = tk.StringVar()

        # Define attributes
        self.categories = get_categories()
        self.areas = get_areas()
        self.all_categories = ""
        self.all_areas = ""
        self.meals = ""
        self.recipe = ""

        # Display Menu
        ttk.Label(self.frame, text="COMMAND MENU").grid(column=0, row=0, sticky="W")

        # Menu Buttons
        ttk.Button(self.frame, text="List all Categories", command=self.display_categories).grid(column=0, row=1, sticky="W")
        ttk.Button(self.frame, text="List all Meals for a Category", command=self.input_category).grid(column=0, row=2, sticky="W")
        ttk.Button(self.frame, text="Search Meal by Name", command=self.input_meal).grid(column=0, row=3, sticky="W")
        ttk.Button(self.frame, text="Random Meal", command=self.display_random_meal).grid(column=0, row=4, sticky="W")
        ttk.Button(self.frame, text="List all Areas", command=self.display_areas).grid(column=0, row=5, sticky="W")
        ttk.Button(self.frame, text="Search Meals by Area", command=self.input_area).grid(column=0, row=6, sticky="W")

        # Displaying the main commands in a multi-line text format
        ttk.Label(self.frame, textvariable=self.display, wraplength=500).grid(column=2, row=0, columnspan=3, rowspan=1000, sticky="N")

    def input_category(self):
        self.category.set("")
        ttk.Label(self.frame, text="Enter a Category:          ").grid(column=0, row=8, sticky="W")
        ttk.Entry(self.frame, textvariable=self.category, width=20).grid(column=0, row=9, sticky="W")
        ttk.Button(self.frame, text="Get Meals", command=self.display_meals_by_category).grid(column=0, row=10, sticky="W")

    def input_meal(self):
        self.meal_name.set("")
        ttk.Label(self.frame, text="Enter Meal Name:      ").grid(column=0, row=8, sticky="W")
        ttk.Entry(self.frame, textvariable=self.meal_name, width=20).grid(column=0, row=9, sticky="W")
        ttk.Button(self.frame, text="Get Meal", command=self.display_meal).grid(column=0, row=10, sticky="W")

    def input_area(self):
        self.area.set("")
        ttk.Label(self.frame, text="Enter an Area:          ").grid(column=0, row=8, sticky="W")
        ttk.Entry(self.frame, textvariable=self.area, width=20).grid(column=0, row=9, sticky="W")
        ttk.Button(self.frame, text="Get Meals", command=self.display_meals_by_area).grid(column=0, row=10, sticky="W")

    def display_meals_by_category(self):
        self.meals = ""
        category_str = self.category.get()
        self.meals = get_meal_str_c(self.meals, category_str)
        self.display.set(self.meals)

    def display_categories(self):
        self.all_categories = "CATEGORIES\n"
        for i in range(len(self.categories)):
            category = self.categories[i]
            self.all_categories += category.get_category() + "\n"
        self.display.set(self.all_categories)

    def display_meals_by_area(self):
        self.meals = ""
        area_str = self.area.get()
        self.meals = get_meal_str_a(self.meals, area_str)
        self.display.set(self.meals)

    def display_areas(self):
        self.all_areas = "AREAS\n"
        for i in range(len(self.areas)):
            area = self.areas[i]
            self.all_areas += area.get_area() + "\n"
        self.display.set(self.all_areas)

    def display_meal(self):
        self.recipe = ""
        meal_str = self.meal_name.get()
        self.recipe = get_recipe_str(self.recipe, meal_str)
        self.display.set(self.recipe)

    def display_random_meal(self):
        random_name = requests.get_random_meal()
        self.recipe = "A random meal was selected just for you!\n\n"
        self.recipe = get_recipe_str(self.recipe, random_name)
        self.display.set(self.recipe)

    def configure_frame(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("My Recipes Program")
    root.geometry("650x275")
    RecipeFrame(root)

    root.mainloop()