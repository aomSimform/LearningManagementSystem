from django.shortcuts import render
from rest_framework import generics, mixins
from .serializers import GradesSerializers
from .models import Gradings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.models import Courses, Subsection
from rest_framework.exceptions import PermissionDenied
from courses.permissions import isInstructor
from courses.models import Subsection
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.




class GradingViewset(generics.ListCreateAPIView):
    serializer_class = GradesSerializers
    permission_classes = [IsAuthenticated]
    queryset = Gradings.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), isInstructor()]
        return [IsAuthenticated()]
    def post(self, request, *args, **kwargs):
        print(request.data)
        return super().post(request, *args, **kwargs)
    def get_queryset(self):
        course = get_object_or_404(
            Courses,
            pk=self.kwargs["course"]
        )
        subsection = get_object_or_404(
            Subsection,
            pk=self.kwargs["subsection"]
        )

        user = self.request.user

        if subsection.course != course:
            raise PermissionDenied(
                "Subsection does not belong to course"
            )

        if user.role == "student":
            if not course.students.filter(
                pk=user.id
            ).exists():
                raise PermissionDenied(
                    "Not enrolled"
                )

            return Gradings.objects.filter(
                user=user,
                assignment__subsection=subsection
            )

        if course.created_by != user:
            raise PermissionDenied(
                "Not allowed"
            )

        return Gradings.objects.filter(
            assignment__subsection=subsection
        )

    def perform_create(self, serializer):
        if self.request.user.role != "instructor":
            raise PermissionDenied(
                "Only instructors can grade"
            )
        serializer.save()


class TotalGradesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course, subsection):

        course_obj = get_object_or_404(
            Courses,
            pk=course
        )

        subsection_obj = get_object_or_404(
            Subsection,
            pk=subsection
        )

        user = request.user

        if subsection_obj.course != course_obj:
            raise PermissionDenied(
                "Subsection does not belong to course"
            )

        if user.role == "student":
            if not course_obj.students.filter(
                pk=user.id
            ).exists():
                raise PermissionDenied(
                    "Not enrolled"
                )

            qs = Gradings.objects.filter(
                user=user,
                assignment__subsection=subsection_obj
            )

        else:

            if course_obj.created_by != user:
                raise PermissionDenied(
                    "Not allowed"
                )

            qs = Gradings.objects.filter(
                assignment__subsection=subsection_obj
            )

        total = qs.aggregate(
            total_grades=Sum("grades")
        )["total_grades"] or 0

        return Response({
            "course": course_obj.id,
            "subsection": subsection_obj.id,
            "user": user.id,
            "total_grades": total
        })