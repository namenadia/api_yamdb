from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, get_token,
                    register_user)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns_auth = [
    path('signup/', register_user, name='register_user'),
    path('token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
