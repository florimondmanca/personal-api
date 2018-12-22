"""URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic.base import RedirectView

from .feeds import LatestPostsFeed
from .sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("markdownx/", include("markdownx.urls")),
    path("api/", include("api.urls")),
    path("blog/feed/", LatestPostsFeed()),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path("", RedirectView.as_view(url="admin", permanent=False), name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
