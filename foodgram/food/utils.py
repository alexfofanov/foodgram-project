from .models import Ingridient, RecipeIngridient, Recipe
from django.db.models import Q


def teg_filter(tag):

    queries = []
    if 'breakfast' in tag:
        queries.append(Q(breakfast=True))
        # breakfast = True

    if 'lunch' in tag:
        queries.append(Q(lunch=True))
        # lunch = True

    if 'dinner' in tag:
        queries.append(Q(dinner=True))
        # dinner = True

    if tag == '':
        recipe_list = Recipe.objects.filter().order_by('-pub_date')
    else:
        query = queries.pop()
        for item in queries:
            query |= item
        recipe_list = Recipe.objects.filter(query).order_by('-pub_date')

    return recipe_list


def get_recipe_ingridients(data):
    ingredient_numbers = set()
    recipe_ingridients = []

    for key in data:
        if key.startswith('nameIngredient_'):
            _, number = key.split('_')
            ingredient_numbers.add(number)

    for number in ingredient_numbers:
        recipe_ingridients.append(
            {
                'name': data[f'nameIngredient_{number}'],
                'unit': data[f'unitsIngredient_{number}'],
                'quantity': float(data[f'valueIngredient_{number}']),
            }
        )

    return recipe_ingridients


def save_recipe_ingridients(recipe, recipe_ingridients):
    for ingridient in recipe_ingridients:
        RecipeIngridient.objects.create(
            recipe=recipe,
            ingridient=Ingridient.objects.get(name=ingridient.get('name')),
            quantity=ingridient.get('quantity'),
        )
