import collections
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import (Favorite, Ingridient, Purchase, Recipe, RecipeIngridient,
                     Subscription, User)
from .utils import get_recipe_ingridients, save_recipe_ingridients, tag_filter


def index(request):
    tag = request.GET.get('tag', '')
    recipe_list = tag_filter(tag)
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    data = {
        'page': page,
        'paginator': paginator,
        'tag': tag,
    }

    return render(request, 'food/index.html', context=data)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = Recipe.objects.create(
            author=request.user,
            name=form.cleaned_data['name'],
            breakfast=form.cleaned_data['breakfast'],
            lunch=form.cleaned_data['lunch'],
            dinner=form.cleaned_data['dinner'],
            time=form.cleaned_data['time'],
            description=form.cleaned_data['description'],
            picture=form.cleaned_data['picture'],
        )
        recipe_ingridients = get_recipe_ingridients(request.POST)
        save_recipe_ingridients(recipe, recipe_ingridients)
        return redirect('food:index')

    return render(request, 'food/formRecipe.html', {'form': form})


def recipe(request, author, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
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
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe_ingridient = RecipeIngridient.objects.filter(recipe=recipe)
        form = RecipeForm(
            request.POST or None, files=request.FILES or None, instance=recipe
        )

        data = {'form': form, 'recipe_ingridient': recipe_ingridient}

        if form.is_valid():
            recipe = form.save()
            recipe_ingridient.delete()
            recipe_ingridients = get_recipe_ingridients(request.POST)
            save_recipe_ingridients(recipe, recipe_ingridients)

            return redirect('food:recipe', author=author, recipe_id=recipe_id)

        return render(request, 'food/formRecipe.html', context=data)
    else:
        return redirect('food:recipe', author=author, recipe_id=recipe_id)


@login_required
def recipe_delete(request, author, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delte()
        return redirect('food:index')

    else:
        return redirect('food:recipe', author=author, recipe_id=recipe_id)


def author_recipe(request, author):
    author = get_object_or_404(User, username=author)

    tag = request.GET.get('tag', '')
    recipe_list = tag_filter(tag).filter(author=author)
    # recipe_list = Recipe.objects.filter(author=author).order_by('-pub_date')

    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {
        'author': author,
        'page': page,
        'paginator': paginator,
        'tag': tag,
    }

    return render(request, 'food/authorRecipe.html', context=data)


@login_required
def subscription(request, username):
    subscription_list = Subscription.objects.filter(
        user=request.user
    ).order_by('id')

    paginator = Paginator(subscription_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    data = {
        'page': page,
        'paginator': paginator,
    }

    return render(request, 'food/follow.html', context=data)


@login_required
def favorite(request, username):
    tag = request.GET.get('tag', '')

    queries = []
    if 'breakfast' in tag:
        queries.append(Q(recipe__breakfast=True))

    if 'lunch' in tag:
        queries.append(Q(recipe__lunch=True))

    if 'dinner' in tag:
        queries.append(Q(recipe__dinner=True))

    if tag == '':
        favorite_list = Favorite.objects.filter(
            user=request.user
        ).order_by('id')
    else:
        query = queries.pop()
        for item in queries:
            query |= item

        favorite_list = Favorite.objects.filter(user=request.user).filter(
            query
        ).order_by('id')

    paginator = Paginator(favorite_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    data = {
        'page': page,
        'paginator': paginator,
        'tag': tag,
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

    with open(settings.MEDIA_ROOT + '/purches.txt', 'w+') as file:
        for name, quantity in purchase_ingridient.items():
            file.write(f'{name} - {quantity}\n')

    response = HttpResponse(
        open(settings.MEDIA_ROOT + '/purches.txt'),
        content_type='application/txt',
    )
    response['Content-Disposition'] = 'attachment; filename="purches.txt"'
    # response['charset'] = 'UTF-8'
    return response


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


# ===== JS requests =====


@login_required
def add_subscription(request):
    if request.method == 'POST':
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        _, created = Subscription.objects.get_or_create(
            user=request.user, author=author
        )

    if created:
        data = [{'success': True}]
    else:
        data = [{'success': False}]

    return JsonResponse(data, safe=False)


@login_required
def remove_subscription(request, author_id):
    author = get_object_or_404(User, id=author_id)
    remove = Subscription.objects.filter(
        user=request.user, author=author
    ).delete()

    if remove:
        data = [{'success': True}]
    else:
        data = [{'success': False}]

    return JsonResponse(data, safe=False)


@login_required
def add_favorite(request):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe
        )

    if created:
        data = [{'success': True}]
    else:
        data = [{'success': False}]

    return JsonResponse(data, safe=False)


@login_required
def remove_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    remove = Favorite.objects.filter(user=request.user, recipe=recipe).delete()

    if remove:
        data = [{'success': True}]
    else:
        data = [{'success': False}]

    return JsonResponse(data, safe=False)


@login_required
def add_purchase(request):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = Purchase.objects.get_or_create(
            user=request.user, recipe=recipe
        )

    if created:
        data = [{'success': True}]
    else:
        data = [{'success': False}]

    return JsonResponse(data, safe=False)


@login_required
def remove_purchase(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    remove = Purchase.objects.filter(user=request.user, recipe=recipe).delete()

    if remove:
        data = [{'success': True}]
    else:
        data = [{'success': False}]

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
        data = [{'success': False}]

    return JsonResponse(data, safe=False)
