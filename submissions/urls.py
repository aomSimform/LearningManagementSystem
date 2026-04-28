from django.urls import path
from .views import GradingViewset

urlpatterns = [
    # List grades for a subsection
    # GET /api/grades/course/1/subsection/5/
    path(
        "course/<int:course>/subsection/<int:subsection>/",
        GradingViewset.as_view(),
        name="grading-list-create",
    ),
]
