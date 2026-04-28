from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CoursesViewSet, SubSectionViewSet, AssignmentsCreateDeleteView

router = DefaultRouter()
router.register(r"", CoursesViewSet, basename="courses")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:pk>/enroll/",
        CoursesViewSet.as_view({"post": "enrolled"}),
        name="course-enroll",
    ),
    path(
        "<int:pk>/deenroll/",
        CoursesViewSet.as_view({"delete": "deenrolled"}),
        name="course-deenroll",
    ),
    path(
        "<int:course>/subsections/",
        SubSectionViewSet.as_view({"get": "list", "post": "create"}),
        name="subsection-list-create",
    ),
    path(
        "<int:course>/subsections/<int:pk>/",
        SubSectionViewSet.as_view({"patch": "partial_update", "delete": "destroy"}),
        name="subsection-detail",
    ),
    path(
        "<int:course>/subsections/<int:subsection>/assignments/",
        AssignmentsCreateDeleteView.as_view(),
        name="assignment-create",
    ),
    path(
        "<int:course>/subsections/<int:subsection>/assignments/<int:pk>/",
        AssignmentsCreateDeleteView.as_view(),
        name="assignment-delete",
    ),
]
