from .views import GradingViewset, TotalGradesView
from django.urls import path
urlpatterns = [
    path(
        "",
        GradingViewset.as_view(),
        name="grading-list-create",
    ),

    path(
        "total/",
        TotalGradesView.as_view(),
        name="grading-total",
    ),
]