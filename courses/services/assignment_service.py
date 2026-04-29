from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from ..models import Subsection


class AssignmentService:

    @staticmethod
    def get_subsection_for_instructor(
        subsection_id,
        user
    ):
        subsection = get_object_or_404(
            Subsection,
            pk=subsection_id
        )

        if subsection.course.created_by != user:
            raise PermissionDenied(
                "You do not have permission"
            )

        return subsection


    @staticmethod
    def delete_assignment(instance):
        assignment_id = instance.id
        instance.delete()

        return {
            "success": (
                f"Assignment {assignment_id} "
                "deleted successfully"
            )
        }