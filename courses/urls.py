from django.urls import path
from .views import CoursesViewSet, SubSectionViewSet
urlpatterns = [
    path('',CoursesViewSet.as_view({'get':'list','post':'create'})),
    path('enrolled/',CoursesViewSet.as_view({'post':'enrolled'})),
    path('<int:pk>/',CoursesViewSet.as_view({"get":"retrieve"})),
    path('delete/<int:pk>/',CoursesViewSet.as_view({"post":"destroy"})),
    path('update/<int:pk>/',CoursesViewSet.as_view({"patch":"partial_update"})),
    path('<int:course>/subsection',SubSectionViewSet.as_view({"get":"list",'post':"create",'patch':"partial_update"})),
    path('<int:course>/subsection/<int:pk>',SubSectionViewSet.as_view({'patch':"partial_update","post":"destroy"}))
]   