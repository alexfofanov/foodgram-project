# from food.models impost Recipe
from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.create_user('alex', 'alex@mail.io', '123')


"""
Recipe.objects.create(
                author=User.get(''),
                name='Французские тосты',
                cooking_time='30',
                description='Смешать молоко с сахаром, добавить яйца, тщательно все взбить.
Обмакнуть тосты в смесь и жарить на сливочном масле до золотистой корочки.
Полить сверху сиропом топинамбура и украсить ягодами.',
                picture=''
            )
"""            