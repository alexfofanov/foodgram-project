from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingridient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name},({self.unit})'


class Tag(models.Model):
    name = models.CharField(max_length=7)
    slug = models.SlugField(unique=True, max_length=15, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True, db_index=True
    )
    name = models.CharField(max_length=50)
    tags = models.ManyToManyField(Tag, related_name="recipes")
    time = models.PositiveSmallIntegerField()
    description = models.TextField()
    picture = models.ImageField(upload_to='recipe/')

    def __str__(self):
        return f'{self.pub_date}, ({self.name})'


class RecipeIngridient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingridients'
    )
    ingridient = models.ForeignKey(
        Ingridient, on_delete=models.CASCADE,
        related_name='recipe_ingridients'
    )
    quantity = models.DecimalField(max_digits=5, decimal_places=0)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites'
    )


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchase'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='purchase'
    )
