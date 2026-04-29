from rest_framework import serializers
from .models import Submissions
from users.models import User




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

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["user"] = {
            "id": instance.user.id,
            "email": instance.user.email,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
        }

        

        return data
