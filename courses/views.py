from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Courses, Subsection, Enrolled, Assignments
from .permissions import (
    isInstructor,
    isStudent,
    isCourseOwner,
    isSubsectionCreatedByInstarctor,
    isAssignmentCretedByInstarctor
)
from .serializers import (
    createCourse,
    enrolledCourse,
    ListCourses,
    studentDetailCourse,
    instructorDetailCourse,
    createSubsection,
    assignmentSerializer
)


# -------------------------
# Courses
# -------------------------

class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(
    is_archived=False
)

        if self.action == "list":
            if user.role == "student":
                return queryset.filter(students=user)

            if user.role == "instructor":
                return queryset.filter(created_by=user)

        return queryset

    def get_permissions(self):
        user = self.request.user

        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated(), isInstructor()]

        if self.action == "retrieve" and user.role == "instructor":
            return [IsAuthenticated(), isCourseOwner()]

        if self.action in ["enroll", "deenroll"]:
            return [IsAuthenticated(), isStudent()]

        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return createCourse

        if self.action == "enroll":
            return enrolledCourse

        if self.action == "list":
            return ListCourses

        if self.action == "retrieve":
            if self.request.user.role == "student":
                return studentDetailCourse
            return instructorDetailCourse

    def destroy(self, request, *args, **kwargs):
        
        #soft delete in case of enrollements or grades exists in courses

        course = self.get_object()

        has_students = course.students.exists()

        has_subsections = (
            course.subsections.exists()
        )

        if has_students or has_subsections:

            course.is_archived = True
            course.save()

            return Response(
                {
                    "success":
                    "Course archived instead of deleted."
                },
                status=status.HTTP_200_OK
            )

        # hard delete
        course.delete()

        return Response(
            {
                "success":
                "Course deleted permanently."
            },
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=["post"])
    def enroll(self, request, pk=None):
        serializer = self.get_serializer(data={"course": pk})
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(
            {"success": "Enrolled successfully"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["delete"])
    def deenroll(self, request, pk=None):
        enrolled = Enrolled.objects.filter(
            course=pk,
            user=request.user
        )

        if not enrolled.exists():
            return Response(
                {"error": "You are not enrolled in this course"},
                status=status.HTTP_400_BAD_REQUEST
            )

        enrolled.delete()

        return Response(
            {"success": "De-enrolled successfully"},
            status=status.HTTP_200_OK
        )


# -------------------------
# Subsections
# -------------------------

class SubSectionViewSet(ModelViewSet):
    queryset = Subsection.objects.prefetch_related("assignments")
    serializer_class = createSubsection
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course = self.get_course()

        if self.action == "list":
            return self.queryset.filter(course=course)

        return self.queryset.filter(
            course=self.kwargs["course"]
        )

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [
                IsAuthenticated(),
                isInstructor(),
                isSubsectionCreatedByInstarctor()
            ]

        return [IsAuthenticated()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["kwargs"] = self.kwargs
        return context

    def perform_create(self, serializer):
        serializer.save(course=self.get_course())

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return Response({
            "success": f"Subsection {kwargs['pk']} deleted successfully"
        })

    def get_course(self):
        course = get_object_or_404(
            Courses,
            pk=self.kwargs["course"]
        )

        if self.request.user.role == "student":
            if not course.students.filter(
                pk=self.request.user.pk
            ).exists():
                raise PermissionDenied(
                    "You are not enrolled in this course."
                )

        else:
            if course.created_by != self.request.user:
                raise PermissionDenied(
                    "You do not have permission for this course."
                )

        return course


# -------------------------
# Assignments
# -------------------------

class AssignmentsCreateDeleteView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Assignments.objects.all()
    serializer_class = assignmentSerializer

    permission_classes = [
        isInstructor,
        isAssignmentCretedByInstarctor
    ]

    def get_subsection(self):
        subsection = get_object_or_404(
            Subsection,
            pk=self.kwargs["subsection"]
        )

        if subsection.course.created_by != self.request.user:
            raise PermissionDenied(
                "You do not have permission for this course"
            )

        return subsection

    def perform_create(self, serializer):
        serializer.save(
            subsection=self.get_subsection()
        )

    def post(self, request, *args, **kwargs):
        return self.create(
            request,
            *args,
            **kwargs
        )

    def delete(self, request, *args, **kwargs):
        self.destroy(
            request,
            *args,
            **kwargs
        )

        return Response({
            "success": f"Assignment {kwargs['pk']} deleted successfully"
        })
