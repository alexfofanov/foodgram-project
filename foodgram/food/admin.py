from django.contrib import admin

from .models import (
    Ingridient,
    Recipe,
    RecipeIngridient,
    Favorite,
    Subscription,
    Purchase,
)


class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'unit',
    )
    search_field = ('name',)
    list_filter = ('name',)


class IngridientInline(admin.TabularInline):
    model = RecipeIngridient
    extra = 1  # number of lines


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngridientInline,)
    list_filter = ('name',)


class RecipeIngridientsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingridient', 'quantity')


class FavoriteAdmin(admin.ModelAdmin):
    pass


class SubscriptionAdmin(admin.ModelAdmin):
    pass


class PurchaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingridient, IngridientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngridient, RecipeIngridientsAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Purchase, PurchaseAdmin)
