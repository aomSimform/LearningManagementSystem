from django.urls import path
from .views import CoursesViewSet, SubSectionViewSet,AssignmentsCreateDeleteView
urlpatterns = [
    path('',CoursesViewSet.as_view({'get':'list','post':'create'})),
    path('enrolled/<int:pk>/',CoursesViewSet.as_view({'get':'enrolled'})),
    path('deenrolled/<int:pk>/',CoursesViewSet.as_view({'get':'deenrolled'})),
    path('<int:pk>/',CoursesViewSet.as_view({"get":"retrieve","delete":"destroy"})),
    path('update/<int:pk>/',CoursesViewSet.as_view({"patch":"partial_update"})),
    path('<int:course>/subsection',SubSectionViewSet.as_view({"get":"list",'post':"create"})),
    path('<int:course>/subsection/<int:pk>',SubSectionViewSet.as_view({'patch':"partial_update","delete":"destroy"})),
    path('<int:course>/subsection/<int:subsection>/assignments',AssignmentsCreateDeleteView.as_view()),
    path('<int:course>/subsection/<int:subsection>/assignments/<int:pk>',AssignmentsCreateDeleteView.as_view())
]   