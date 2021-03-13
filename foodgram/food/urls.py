from django.urls import path

from . import views

app_name = 'food'

urlpatterns = [
    path('', views.index, name='index'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('favorites/', views.add_favorite, name='add_favorite'),
    path(
        'favorites/<int:recipe_id>/',
        views.remove_favorite,
        name='remove_favorite',
    ),
    path('subscriptions/', views.add_subscription, name='add_subscription'),
    path(
        'subscriptions/<int:author_id>/',
        views.remove_subscription,
        name='remove_subscription',
    ),
    path('purchases/', views.add_purchase, name='add_purchase'),
    path(
        'purchases/<int:recipe_id>/',
        views.remove_purchase,
        name='remove_purchase',
    ),
    path('new/', views.new_recipe, name='new_recipe'),
    path('<str:author>/', views.author_recipe, name='author_recipe'),
    path('<str:author>/<int:recipe_id>/', views.recipe, name='recipe'),
    path(
        '<str:author>/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='recipe_edit',
    ),
    path(
        '<str:author>/<int:recipe_id>/delete/',
        views.recipe_delete,
        name='recipe_delete',
    ),
    path('<str:username>/purchase/', views.purchase, name='purchase'),
    path(
        '<str:username>/subscription/',
        views.subscription,
        name='subscription'
    ),
    path('<str:username>/favorite/', views.favorite, name='favorite'),
    path(
        '<str:username>/purchase_download/',
        views.purchase_download,
        name='purchase_download',
    ),
]
