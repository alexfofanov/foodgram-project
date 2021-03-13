from django.shortcuts import get_object_or_404

from .models import Ingridient, Recipe, RecipeIngridient, Tag


def tag_filter(filter):
    if filter == '':
        return Recipe.objects.all().order_by("-pub_date")

    tags = Tag.objects.all()
    tags_filter = [tag.slug for tag in tags if tag.slug in filter]

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
            ingridient=get_object_or_404(Ingridient,
                                         name=ingridient.get('name')),
            quantity=ingridient.get('quantity'),
        )
