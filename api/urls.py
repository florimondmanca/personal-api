"""API URLs."""

from rest_framework.routers import DefaultRouter

import blog.views

# Enable view names as 'api:...'
app_name = 'api'

router = DefaultRouter()

# Blog endpoints
router.register('posts', blog.views.PostViewSet)


urlpatterns = router.urls
