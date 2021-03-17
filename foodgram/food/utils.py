from django.shortcuts import get_object_or_404

from .models import Ingridient, Recipe, RecipeIngridient, Tag


def tag_filter(filter):
    if len(filter) == 0:
        return Recipe.objects.all().order_by("-pub_date")

    tags_filter = Tag.objects.values_list(
        'slug', flat=True).filter(slug__in=filter)

    recipe_list = Recipe.objects.filter(
        tags__slug__in=tags_filter).order_by("-pub_date").distinct()

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
                'id': number,
                'name': data[f'nameIngredient_{number}'],
                'unit': data[f'unitsIngredient_{number}'],
                'quantity': int(data[f'valueIngredient_{number}']),
            }
        )
    return recipe_ingridients


def save_recipe_ingridients(recipe, recipe_ingridients):
    for ingridient in recipe_ingridients:
        RecipeIngridient.objects.create(
            recipe=recipe,
            ingridient=get_object_or_404(Ingridient,
                                         name=ingridient.get('name')),
            quantity=ingridient.get('quantity'),
        )


def is_quantity_positive(recipe_ingridients):
    for ingridient in recipe_ingridients:
        if ingridient.get('quantity') < 0:
            return False
    return True


def is_form_errors(data):
    recipe_ingridients_form = get_recipe_ingridients(data)
    recipe_tags_form_id = data.getlist('tags')
    error_msg = ''
    if not recipe_ingridients_form:
        error_msg += 'Пожалуйста, добавте ингридиент. \n'
    if not is_quantity_positive(recipe_ingridients_form):
        error_msg += 'Пожалуйста, исправте отрицательное количество. \n'
    if not recipe_tags_form_id:
        error_msg += 'Пожалуйста, добавте хотя бы один тег. \n'

    return error_msg


def recipe_ingridients_list(recipe):
    recipe_ingridients = RecipeIngridient.objects.filter(recipe=recipe)
    recipe_ingridients_list = []
    for ingridient in recipe_ingridients:
        recipe_ingridients_list.append(
            {   
                'id': ingridient.id,
                'name': ingridient.ingridient.name,
                'unit': ingridient.ingridient.unit,
                'quantity': ingridient.quantity
            }
        )
    return recipe_ingridients_list
