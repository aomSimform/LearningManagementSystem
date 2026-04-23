from django.urls import path
from .views import CoursesViewSet
urlpatterns = [
    path('',CoursesViewSet.as_view({'get':'list','post':'create'})),
    path('enrolled/',CoursesViewSet.as_view({'post':'enrolled'}))
]   