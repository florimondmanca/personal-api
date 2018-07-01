"""API URLs."""

from rest_framework.routers import DefaultRouter

import blog.api

# Enable view names as 'api:...'
app_name = 'api'

router = DefaultRouter()

# Blog endpoints
router.register('posts', blog.api.PostViewSet)


urlpatterns = router.urls
