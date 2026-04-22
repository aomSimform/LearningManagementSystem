from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
class UserSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(write_only=True)
    
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
        
        