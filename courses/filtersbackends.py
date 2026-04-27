<<<<<<< HEAD
from rest_framework.filters import BaseFilterBackend
from django.core.exceptions import ValidationError

class SubsectionFilter(BaseFilterBackend):
    def filter_queryset(self,request,queryset, view):
        return queryset.filter(course = self.kwargs.get('course'))
=======
from rest_framework.filters import BaseFilterBackend
from django.core.exceptions import ValidationError

class SubsectionFilter(BaseFilterBackend):
    def filter_queryset(self,request,queryset, view):
        return queryset.filter(course = self.kwargs.get('course'))
>>>>>>> fb2d2e087fc74deb708398fda7513f10b81ef9c2
    