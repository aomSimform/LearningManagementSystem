from django.urls import include, path 
from .views import registerViewSet


urlpatterns = [
    path('register/',registerViewSet.as_view(),name = 'register')
]