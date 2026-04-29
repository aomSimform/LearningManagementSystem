from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from ..models import Courses, Subsection


class SubSectionService:

    @staticmethod
    def get_course_for_user(course_id, user):
        course = get_object_or_404(
            Courses,
            pk=course_id
        )

        if user.role == "student":
            if not course.students.filter(
                pk=user.pk
            ).exists():
                raise PermissionDenied(
                    "You are not enrolled in this course"
                )

        elif course.created_by != user:
            raise PermissionDenied(
                "You do not have permission"
            )

        return course


    @staticmethod
    def list_subsections(course_id, user):
        course = SubSectionService.get_course_for_user(
            course_id,
            user
        )

        return Subsection.objects.filter(
            course=course
        )


    @staticmethod
    def delete_subsection(instance):
        subsection_id = instance.id
        instance.delete()

        return {
            "success": f"Subsection {subsection_id} deleted successfully"
        }