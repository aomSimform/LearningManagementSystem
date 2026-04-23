from django.urls import include, path 
from .views import registerViewSet,LoginViewSet

from rest_framework_simplejwt.views import TokenBlacklistView


urlpatterns = [
    path('register/',registerViewSet.as_view(),name = 'register'),
    path('login/',LoginViewSet.as_view(),name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist')
]