from django.urls import path
from .views import submissionListCreate

urlpatterns = [

    path(
        "",
        submissionListCreate.as_view(),
        name="submissions",
    ),
]
