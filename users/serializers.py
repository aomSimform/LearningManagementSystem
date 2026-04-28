from rest_framework import serializers
from .models import User, InstructorProfile, StudentProfile
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model 
from .backends import CustomBackend

USER = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ["id", "first_name","last_name", "email"]

class UserCreationSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only = True)
    user = UserSerializer()
        
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
        depth=1
        fields = ['role','email','password','first_name','last_name','confirm_password','user']
        
        
        
        
        
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



class UserSerailizer(serializers.ModelSerializer):
    class Meta:
        model=USER
        fields = '__all__'
        
        
        
        

class StudentProfileSerailizers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = StudentProfile
        fields='__all__'
        
class InstructorProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = InstructorProfile
        fields = '__all__'
