from django.urls import path
from .views import submissionListCreate

urlpatterns = [

    path(
        "course/<int:course>/subsection/<int:subsection>/",
        submissionListCreate.as_view(),
        name="submissions",
    ),
]
