import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from food.models import Recipe, RecipeIngridient, Ingridient, Tag

User = get_user_model()


def create_recipes(author, number):
    # author = User.objects.get(username=author)

    tags = [Tag.objects.get(slug='breakfast'),
            Tag.objects.get(slug='lunch'),
            Tag.objects.get(slug='dinner')]

    for _ in range(number):
        recipe = Recipe.objects.create(
            author=author,
            name='Французские тосты',
            time='30',
            description='Смешать молоко с сахаром, добавить яйца, тщательно все взбить. \
Обмакнуь тосты в смесь и жарить на сливочном масле до золотистой корочки. \
Полить верху сиропом топинамбура и украсить ягодами.',
            picture='recipe/french_toast.png'
        )

        recipe.tags.add(random.choice(tags))

        RecipeIngridient.objects.create(
            recipe=recipe,
            ingridient=Ingridient.objects.get(name='яйца куриные'),
            quantity=2
        )
        RecipeIngridient.objects.create(
            recipe=recipe,
            ingridient=Ingridient.objects.get(name='молоко'),
            quantity=200
        )
        RecipeIngridient.objects.create(
            recipe=recipe,
            ingridient=Ingridient.objects.get(name='гренки'),
            quantity=4
        )
        RecipeIngridient.objects.create(
            recipe=recipe,
            ingridient=Ingridient.objects.get(name='сахар'),
            quantity=2
        )
        RecipeIngridient.objects.create(
            recipe=recipe,
            ingridient=Ingridient.objects.get(name='ягоды'),
            quantity=100
        )
        RecipeIngridient.objects.create(
            recipe=recipe,
            ingridient=Ingridient.objects.get(name='топинамбур'),
            quantity=3
        )


class Command(BaseCommand):
    help = 'Create new recipe'

    def handle(self, *args, **options):
        create_recipes(
            User.objects.create_user('leo',
                                     'leo@mail.io',
                                     '123',
                                     first_name='Лев Толстой'), 10
        )

        create_recipes(
            User.objects.create_user('mike',
                                     'mike@mail.io',
                                     '123',
                                     first_name='Михаил Булгаков'), 1
        )

        create_recipes(
            User.objects.create_user('fedor',
                                     'fedor@mail.io',
                                     '123',
                                     first_name='Фёдор Достоевский'), 2
        )

        create_recipes(
            User.objects.create_user('anton',
                                     'anton@mail.io',
                                     '123',
                                     first_name='Антон Чехов'), 3
        )

        create_recipes(
            User.objects.create_user('ivan',
                                     'ivan@mail.io',
                                     '123',
                                     first_name='Иван Тургенев'), 7
        )

        create_recipes(
            User.objects.create_user('niko',
                                     'niko@mail.io',
                                     '123',
                                     first_name='Николай Гоголь'), 5
        )
