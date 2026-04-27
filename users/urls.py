from django.urls import include, path 
from .views import registerViewSet,LoginViewSet, ProfileView

from rest_framework_simplejwt.views import TokenBlacklistView

