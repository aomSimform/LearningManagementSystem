from rest_framework import serializers
from .models import Submissions


class SubmissionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Submissions
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Submissions.objects.all(),
                fields=["user", "assignment"],
                message="You already submitted this assignment"
            )
        ]
