from django.shortcuts import render
from rest_framework import generics, mixins
from .serializers import SubmissionSerializer
from .models import Submissions
from courses.models import Courses, Subsection, Assignments
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from courses.permissions import isStudent, isInstructor
from django.shortcuts import get_object_or_404
# Create your views here.


class submissionListCreate(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return self.get_submissions()
    def get(self,request,*args,**kwargs):
        return self.list(request,args,**kwargs)
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

    def get_submissions(self):
        course = get_object_or_404(Courses,pk = self.kwargs['course'])
        subsection = get_object_or_404(Subsection, pk=self.kwargs['subsection'])
        user = self.request.user
        if not course.subsections.filter(course=course).exists():
            raise PermissionDenied("subsection does not belongs to this course")
        if user.role=='student':
            if not course.students.filter(pk=user.id).exists():
                raise PermissionDenied("you are not enrolled in this course")
            return Submissions.objects.filter(assignment__subsection=subsection,user=user)
        else:
            if not course.created_by==user:
                raise PermissionDenied("you are not allowed to see submissions")
            return Submissions.objects.filter(assignment__subsection=subsection)




