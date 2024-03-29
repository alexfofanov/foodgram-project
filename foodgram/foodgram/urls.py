from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('', include('food.urls')),
    path(
        'about/author/',
        views.flatpage,
        {'url': '/author/'},
        name='author',
    ),
    path(
        'about/tech/',
        views.flatpage,
        {'url': '/tech/'},
        name='tech',
    ),
]

handler404 = 'foodgram.views.page_not_found'
handler500 = 'foodgram.views.server_error'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
