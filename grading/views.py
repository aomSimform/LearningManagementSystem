<<<<<<< HEAD
from django.shortcuts import render
from rest_framework import generics, mixins
from .serializers import GradesSerializers
from .models import Gradings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.models import Courses, Subsection
from rest_framework.exceptions import PermissionDenied
from courses.permissions import isInstructor
# Create your views here.




class GradingViewset(generics.ListCreateAPIView):
    serializer_class = GradesSerializers
    queryset = Gradings.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.get_grades()
    
    def get_permission(self):
        if self.action=='create':
            return [permission() for permission in self.permission_classes]+[isInstructor]
        return super().get_permission()
    def perform_create(self,serializer):
        if self.request.user.role!='student':
            raise PermissionDenied('you are not allowed to submit the assignment')
        print('ndvnuvndvn')     
        course = get_object_or_404(Courses,pk = self.kwargs['course'])
        subsection = get_object_or_404(Subsection, pk=self.kwargs['subsection'])
        user = self.request.user
        if not course.subsections.filter(course=course.id).exists():
            raise PermissionDenied("subsection does not belongs to this course")
        if not course.students.filter(pk=user.id).exists():
            raise PermissionDenied("you are not enrolled in this course")
        return serializer.save(user=self.request.user)
    def get_grades(self):
        course = get_object_or_404(Courses, pk = self.kwargs['course'])
        subsection = get_object_or_404(subsection, pk=self.kwargs['subsection'])
        user = self.request.user
        if not subsection.course!=course:
            raise PermissionDenied('subsection does not belongs to this course')
        if user.role=='student':
            if not course.students.filter(pk=user.id).exists():
                raise PermissionDenied("you are not enrolled in this course")
            return self.queryset.filter(user = user, assignments__subsection__course = course)
        else:
            if not course.created_by==user:
                raise PermissionDenied("you are not allowed to access this course")
            return self.queryset.filter(assignments__subsection__course = course)
        
        
=======
from django.shortcuts import render
from rest_framework import generics, mixins
from .serializers import GradesSerializers
from .models import Gradings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.models import Courses, Subsection
from rest_framework.exceptions import PermissionDenied
from courses.permissions import isInstructor
# Create your views here.




class GradingViewset(generics.ListCreateAPIView):
    serializer_class = GradesSerializers
    queryset = Gradings.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.get_grades()
    
    def get_permission(self):
        if self.action=='create':
            return [permission() for permission in self.permission_classes]+[isInstructor]
        return super().get_permission()
    def perform_create(self,serializer):
        if self.request.user.role!='student':
            raise PermissionDenied('you are not allowed to submit the assignment')
        print('ndvnuvndvn')     
        course = get_object_or_404(Courses,pk = self.kwargs['course'])
        subsection = get_object_or_404(Subsection, pk=self.kwargs['subsection'])
        user = self.request.user
        if not course.subsections.filter(course=course.id).exists():
            raise PermissionDenied("subsection does not belongs to this course")
        if not course.students.filter(pk=user.id).exists():
            raise PermissionDenied("you are not enrolled in this course")
        return serializer.save(user=self.request.user)
    def get_grades(self):
        course = get_object_or_404(Courses, pk = self.kwargs['course'])
        subsection = get_object_or_404(subsection, pk=self.kwargs['subsection'])
        user = self.request.user
        if not subsection.course!=course:
            raise PermissionDenied('subsection does not belongs to this course')
        if user.role=='student':
            if not course.students.filter(pk=user.id).exists():
                raise PermissionDenied("you are not enrolled in this course")
            return self.queryset.filter(user = user, assignments__subsection__course = course)
        else:
            if not course.created_by==user:
                raise PermissionDenied("you are not allowed to access this course")
            return self.queryset.filter(assignments__subsection__course = course)
        
        
>>>>>>> fb2d2e087fc74deb708398fda7513f10b81ef9c2
        