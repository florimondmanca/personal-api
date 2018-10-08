"""API URLs."""

from django.urls import path
from rest_framework.routers import DefaultRouter

import blog.views
from .views import obtain_auth_token

# Enable view names as 'api:...'
app_name = 'api'

router = DefaultRouter()

# Blog endpoints
router.register('posts', blog.views.PostViewSet)
router.register('drafts', blog.views.DraftViewSet)


urlpatterns = router.urls + [
    path('login/', obtain_auth_token)
]
