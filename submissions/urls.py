<<<<<<< HEAD
from django.urls import path, include 
from .views import submissionListCreate


urlpatterns=[
    path('',submissionListCreate.as_view())
=======
from django.urls import path, include 
from .views import submissionListCreate


urlpatterns=[
    path('',submissionListCreate.as_view())
>>>>>>> fb2d2e087fc74deb708398fda7513f10b81ef9c2
]