from rest_framework import serializers 
from .models import Gradings

class GradesSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True,default = serializers.CurrentUserDefault())
    class Meta:
        model = Gradings
        fileds = '__all__'
        read_only_fields = ['user']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Gradings.objects.all(),
                fields=["user", "assignment"],
                message="You are already enrolled in this course."
            )
        ]