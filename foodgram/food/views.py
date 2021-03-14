import collections
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import (Favorite, Ingridient, Purchase, Recipe, RecipeIngridient,
                     Subscription, User, Tag)
from .utils import get_recipe_ingridients, save_recipe_ingridients, tag_filter


def index(request):
    filter = request.GET.get('filter', '')
    recipe_list = tag_filter(filter)
    paginator = Paginator(recipe_list, settings.PAGINATOR_NUM_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    data = {
        'page': page,
        'paginator': paginator,
        'filter': filter
    }

    return render(request, 'food/index.html', context=data)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe_ingridients = get_recipe_ingridients(request.POST)
        save_recipe_ingridients(recipe, recipe_ingridients)
        form.save_m2m()
        return redirect('food:index')

    tags = Tag.objects.all()
    data = {
        'form': form,
        'tags': tags,
        'edit_flag': False,
    }

    return render(request, 'food/formRecipe.html', context=data)


def recipe(request, author, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=author)
    ingridient_list = RecipeIngridient.objects.select_related(
        'ingridient'
    ).filter(recipe_id=recipe)

    data = {
        'recipe': recipe,
        'ingridients': ingridient_list,
    }

    return render(request, 'food/recipe.html', context=data)


@login_required
def recipe_edit(request, author, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=author)
    if request.user != recipe.author:
        return redirect('food:recipe', author=author, recipe_id=recipe_id)

    recipe_ingridient = RecipeIngridient.objects.filter(recipe=recipe)

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )

    if form.is_valid():
        recipe = form.save()
        recipe_ingridient.delete()
        recipe_ingridients = get_recipe_ingridients(request.POST)
        save_recipe_ingridients(recipe, recipe_ingridients)
        return redirect('food:recipe', author=author, recipe_id=recipe_id)

    tags = Tag.objects.all()
    recipe_tags = recipe.tags.values_list('slug', flat=True)
    data = {
        'form': form,
        'tags': tags,
        'recipe_ingridient': recipe_ingridient,
        'recipe_tags': recipe_tags,
        'recipe_id': recipe.id,
        'edit_flag': True,
    }

    return render(request, 'food/formRecipe.html', context=data)


@login_required
def recipe_delete(request, author, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=author)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('food:index')

    return redirect('food:recipe', author=author, recipe_id=recipe_id)


def author_recipe(request, author):
    author = get_object_or_404(User, username=author)
    filter = request.GET.get('filter', '')
    recipe_list = tag_filter(filter).filter(author=author)
    paginator = Paginator(recipe_list, settings.PAGINATOR_NUM_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {
        'author': author,
        'page': page,
        'paginator': paginator,
        'filter': filter,
    }

    return render(request, 'food/authorRecipe.html', context=data)


@login_required
def subscription(request, username):
    subscription_list = Subscription.objects.filter(
        user=request.user
    ).order_by('id')

    paginator = Paginator(subscription_list, settings.PAGINATOR_NUM_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    data = {
        'page': page,
        'paginator': paginator,
    }

    return render(request, 'food/follow.html', context=data)


@login_required
def favorite(request, username):
    filter = request.GET.get('filter', '')

    recipe_list = tag_filter(filter)
    favorite_recipe_list = recipe_list.filter(favorites__user=request.user)

    paginator = Paginator(favorite_recipe_list,
                          settings.PAGINATOR_NUM_PER_PAGE)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    data = {
        'page': page,
        'paginator': paginator,
        'filter': filter,
    }

    return render(request, 'food/favorite.html', context=data)


@login_required
def purchase(request, username):
    purchase_list = Purchase.objects.filter(user=request.user)
    data = {
        'purchase_list': purchase_list,
    }

    return render(request, 'food/shopList.html', context=data)


@login_required
def purchase_download(request, username):
    purchase_list = Purchase.objects.filter(user=request.user)

    purchase_ingridient = collections.Counter()
    for purchase in purchase_list:
        ingridient_list = RecipeIngridient.objects.filter(
            recipe=purchase.recipe
        )
        for ingridient in ingridient_list:
            purchase_ingridient[ingridient.ingridient] += int(
                ingridient.quantity
            )

    purches_text = ''
    for name, quantity in purchase_ingridient.items():
        purches_text += f'{name} - {quantity}\n'

    response = HttpResponse(purches_text,
                            content_type='application/text charset=utf-8')

    response['Content-Disposition'] = 'attachment; filename="purchases.txt"'
    return response


# ===== JS requests =====

@login_required
def add_subscription(request):
    if request.method == 'POST':
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        _, created = Subscription.objects.get_or_create(
            user=request.user, author=author
        )

    data = {'success': created}

    return JsonResponse(data, safe=False)


@login_required
def remove_subscription(request, author_id):
    author = get_object_or_404(User, id=author_id)
    remove = Subscription.objects.filter(
        user=request.user, author=author
    ).delete()

    data = {'success': remove}

    return JsonResponse(data, safe=False)


@login_required
def add_favorite(request):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe
        )

    data = {'success': created}

    return JsonResponse(data, safe=False)


@login_required
def remove_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    remove = Favorite.objects.filter(user=request.user, recipe=recipe).delete()

    data = {'success': remove}

    return JsonResponse(data, safe=False)


@login_required
def add_purchase(request):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = Purchase.objects.get_or_create(
            user=request.user, recipe=recipe
        )

    data = {'success': created}

    return JsonResponse(data, safe=False)


@login_required
def remove_purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    remove = Purchase.objects.filter(user=request.user, recipe=recipe).delete()

    data = {'success': remove}

    return JsonResponse(data, safe=False)


def ingredients(request):
    query = request.GET.get('query')
    ingredients_query = Ingridient.objects.filter(name__startswith=query)
    if ingredients_query:
        data = [
            {'title': ingredient.name, 'dimension': ingredient.unit}
            for ingredient in ingredients_query
        ]
    else:
        data = {'success': False}

    return JsonResponse(data, safe=False)
