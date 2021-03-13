from django import template

from food.models import Favorite, Subscription, Purchase, Recipe, Tag

register = template.Library()


@register.filter
def purchase_count(user):
    if user.is_authenticated:
        return Purchase.objects.filter(user=user).count()
    else:
        return 0


@register.filter
def is_favorite(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def is_subscription(author, user):
    return Subscription.objects.filter(user=user, author=author).exists()


@register.filter
def is_purchase(recipe, user):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def last_three_recipe(author):
    recipe_list = Recipe.objects.filter(
        author=author).order_by('-pub_date')[:3]

    return recipe_list


@register.filter
def recipe_count(author):
    recipe_count = Recipe.objects.filter(author=author).count() - 3
    return recipe_count


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def get_all_tags(x):
    return Tag.objects.all()
