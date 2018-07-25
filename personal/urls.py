"""URL configuration."""

from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .feeds import LatestPostsFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('api/', include('api.urls')),
    path('blog/feed/', LatestPostsFeed()),
    path('', RedirectView.as_view(url='admin', permanent=False), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
