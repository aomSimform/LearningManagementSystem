from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from ..models import Courses, Enrolled


class CourseService:

    @staticmethod
    def list_courses_for_user(user):
        if user.role == "student":
            return Courses.objects.filter(students=user)

        if user.role == "instructor":
            return Courses.objects.filter(created_by=user)

        return Courses.objects.none()


    @staticmethod
    def enroll_student(course_id, user, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return {
            "success": "Enrolled successfully"
        }


    @staticmethod
    def deenroll_student(course_id, user):
        enrollment = Enrolled.objects.filter(
            course=course_id,
            user=user
        )

        if not enrollment.exists():
            raise PermissionDenied(
                "You are not enrolled in this course"
            )

        enrollment.delete()

        return {
            "success": "De-enrolled successfully"
        }


    @staticmethod
    def delete_course(instance):
        course_id = instance.id
        instance.delete()

        return {
            "success": f"Course {course_id} deleted successfully"
        }