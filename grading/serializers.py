from rest_framework import serializers 
from .models import Gradings
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name"]



class GradesSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    user_details = UserSerializer(
        source="user",
        read_only=True
    )

    def validate_grades(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                "Grade must be between 0 and 100."
            )
        return value

    class Meta:
        model = Gradings
        fields = "__all__"

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Gradings.objects.all(),
                fields=["user", "assignment"],
                message="Grade already exists."
            )
        ]