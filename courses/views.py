from django.shortcuts import get_object_or_404
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import generics, mixins, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
import cloudinary.uploader
from submissions.models import Submissions

from .models import Courses, Subsection, Enrolled, Assignments
from .permissions import (
    isInstructor,
    isStudent,
    isCourseOwner,
    isSubsectionCreatedByInstarctor,
    isAssignmentCretedByInstarctor,
)
from .serializers import (
    createCourse,
    enrolledCourse,
    ListCourses,
    studentDetailCourse,
    instructorDetailCourse,
    createSubsection,
    assignmentSerializer,
)

# Courses


class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    permission_classes = []
    throttle_classes = [ScopedRateThrottle]

    def get_throttles(self):
        if self.action == "enroll":
            self.throttle_scope = "enroll"

        elif self.action == "create":
            self.throttle_scope = "course_create"

        return super().get_throttles()

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(is_archived=False)
        if user.is_anonymous:
            return queryset
        print(user.is_anonymous)
        if self.action == "list":
            # if user.role == "student":
            #     return queryset.filter(students=user)

            if user.role == "instructor":
                return queryset.filter(created_by=user)

            return queryset.all()

        return queryset

    def get_permissions(self):
        user = self.request.user

        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated(), isInstructor()]

        if self.action == "retrieve" and user.role == "instructor":
            return [IsAuthenticated(), isCourseOwner()]

        if self.action in ["enroll", "deenroll"]:
            return [IsAuthenticated(), isStudent()]

        return []

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

        # soft delete in case of enrollements or grades exists in courses

        course = self.get_object()
        Assignment = Assignments.objects.get(pk=kwargs.get("pk"))

        has_students = Submissions.assignment.filter(id=Assignment.id).exists()

        has_subsections = course.subsections.exists()

        if has_students or has_subsections:
            course.is_archived = True
            course.save()

            return Response(
                {"success": "Course archived instead of deleted."},
                status=status.HTTP_200_OK,
            )

        # hard delete
        course.delete()

        return Response(
            {"success": "Course deleted permanently."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=True, methods=["post"])
    def enroll(self, request, pk=None):
        try:
            with transaction.atomic():
                # Lock course row until transaction finishes
                course = Courses.objects.select_for_update().get(pk=pk)

                # -------- Edge Case 1 --------
                # Archived course
                if course.is_archived:
                    raise ValidationError("Cannot enroll in archived course.")

                # -------- Edge Case 2 --------
                # Duplicate enrollment
                if Enrolled.objects.filter(course=course, user=request.user).exists():
                    raise ValidationError("Already enrolled.")

                # -------- Edge Case 3 --------
                # Course full
                if course.students.count() >= course.seats:
                    raise ValidationError("Course is full.")

                # Safe insert
                Enrolled.objects.create(course=course, user=request.user)

            return Response(
                {"success": "Enrolled successfully"}, status=status.HTTP_200_OK
            )

        except IntegrityError:
            raise ValidationError("Enrollment conflict occurred.")

    @action(detail=True, methods=["delete"])
    def deenroll(self, request, pk=None):
        enrolled = Enrolled.objects.filter(course=pk, user=request.user)

        if not enrolled.exists():
            return Response(
                {"error": "You are not enrolled in this course"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        enrolled.delete()

        return Response(
            {"success": "De-enrolled successfully"}, status=status.HTTP_200_OK
        )


# Subsections


class SubSectionViewSet(ModelViewSet):
    queryset = Subsection.objects.prefetch_related("assignments")
    serializer_class = createSubsection
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course = self.get_course()

        if self.action == "list":
            return self.queryset.filter(course=course)

        return self.queryset.filter(course=self.kwargs["course"])

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [
                IsAuthenticated(),
                isInstructor(),
                isSubsectionCreatedByInstarctor(),
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

        return Response({"success": f"Subsection {kwargs['pk']} deleted successfully"})

    def get_course(self):
        course = get_object_or_404(Courses, pk=self.kwargs["course"])

        if self.request.user.role == "student":
            if not course.students.filter(pk=self.request.user.pk).exists():
                raise PermissionDenied("You are not enrolled in this course.")

        else:
            if course.created_by != self.request.user:
                raise PermissionDenied("You do not have permission for this course.")

        return course


# Assignments


class AssignmentsCreateDeleteView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = Assignments.objects.filter(is_archived=False)

    serializer_class = assignmentSerializer

    permission_classes = [isInstructor, isAssignmentCretedByInstarctor]

    def get_serializer_context(self):

        context = super().get_serializer_context()

        context["kwargs"] = self.kwargs

        return context

    def get_subsection(self):

        subsection = get_object_or_404(Subsection, pk=self.kwargs["subsection"])

        if subsection.course_id != int(self.kwargs["course"]):
            raise PermissionDenied("Subsection does not belong to course.")

        if subsection.course.created_by != self.request.user:
            raise PermissionDenied("No permission.")

        if subsection.is_archived:
            raise PermissionDenied("Subsection archived.")

        return subsection

    def perform_create(self, serializer):

        uploaded_file = self.request.FILES.get("uploaded_file")

        if not uploaded_file:
            raise ValidationError("File required.")

        result = cloudinary.uploader.upload(
            uploaded_file, resource_type="raw", folder="assignments"
        )

        serializer.save(
            subsection=self.get_subsection(),
            assignment_url=result["secure_url"],
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
        )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        assignment = self.get_object()
        has_students = Submissions.objects.all()

        print("mnfknvn", has_students)
        # if submissions exist archive delete
        if has_students.exists():
            assignment.is_archived = True
            assignment.save()

            print("ass:-", assignment)

            return Response({"success": "Assignment archived."})

        # hard delete
        assignment.delete()

        return Response({"success": "Assignment deleted."})
