from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingridient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name},({self.unit})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipe_author'
    )
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True, db_index=True
    )
    name = models.CharField(max_length=50)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    time = models.CharField(max_length=3)
    description = models.TextField()
    picture = models.ImageField(upload_to='recipe/')
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.pub_date}, ({self.name})'


class RecipeIngridient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_id'
    )
    ingridient = models.ForeignKey(
        Ingridient, on_delete=models.CASCADE, related_name='ingridient_id'
    )
    quantity = models.DecimalField(max_digits=3, decimal_places=0)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscription_user'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscription_author'
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_user'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_recipe'
    )


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_user'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_recipe'
    )
