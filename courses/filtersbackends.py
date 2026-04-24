from rest_framework.filters import BaseFilterBackend
from django.core.exceptions import ValidationError

class SubsectionFilter(BaseFilterBackend):
    def filter_queryset(self,request,queryset, view):
        if queryset.filter(course = view.kwargs['course']).exists():
            queryset.filter(course = view.kwargs['course'])
        return queryset
    