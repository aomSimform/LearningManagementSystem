from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model 
from .backends import CustomBackend
from .models import User, StudentProfile, InstructorProfile

USER = get_user_model()


class UserCreationSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only = True)
    
    def validate_role(self,value):
        if value=='Student':
            print(value)
        print(value)
        return value
        
    def validate(self,kwargs):
        if kwargs['password']!=kwargs['confirm_password']:
            raise ValidationError('password and confirm password must be same') 
        return kwargs
    

    def create(self,validated_data):
        re_password = validated_data.pop('confirm_password')
        print("validate_data:- ",validated_data)
        return User.objects.create_user(**validated_data)
    class Meta:
        model = User 
        fields = ['role','email','password','first_name','last_name','confirm_password']
        
        
        
        
        
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
    def validate(self,kwargs):
        print(kwargs)
        user = authenticate(
        request=self.context.get('request'),
        username=kwargs['email'],   
        password=kwargs['password']
    )
        print(user)
        if not user:
            raise ValidationError("username or password is incorrect or user is not allowed")
        return kwargs

        


class ProfileSerializer(serializers.ModelSerializer):
    # expose nested profile fields
    interests = serializers.CharField(required=False, allow_blank=True)
    expertise = serializers.CharField(required=False, allow_blank=True)
    experience_years = serializers.IntegerField(required=False)
    qualification = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "is_instructor_approved",
            "interests",
            "expertise",
            "experience_years",
            "qualification",
        ]
        read_only_fields = ["email", "role", "is_instructor_approved"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.role == "student" and hasattr(instance, "studentprofile"):
            data["interests"] = instance.studentprofile.interests

        if instance.role == "instructor" and hasattr(instance, "instructorprofile"):
            data["expertise"] = instance.instructorprofile.expertise
            data["experience_years"] = instance.instructorprofile.experience_years
            data["qualification"] = instance.instructorprofile.qualification

        return data

    def update(self, instance, validated_data):
        # update User fields
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()

        if instance.role == "student":
            profile, _ = StudentProfile.objects.get_or_create(user=instance)
            if "interests" in validated_data:
                profile.interests = validated_data["interests"]
                profile.save()

        # update Instructor profile
        if instance.role == "instructor":
            profile, _ = InstructorProfile.objects.get_or_create(user=instance)
            if "expertise" in validated_data:
                profile.expertise = validated_data["expertise"]

            if "experience_years" in validated_data:
                profile.experience_years = validated_data["experience_years"]

            if "qualification" in validated_data:
                profile.qualification = validated_data["qualification"]

            profile.save()

        return instance
        
