from django.urls import path, include 
from .views import submissionListCreate


urlpatterns=[
    path('',submissionListCreate.as_view())
]