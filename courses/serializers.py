from rest_framework import serializers
from .models import Courses, Enrolled, Subsection, Assignments
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class createCourse(serializers.ModelSerializer):
    def create(self,validated_data):
        validated_data['created_by']=self.context.get('request').user
        return Courses.objects.create(**validated_data)
    def update(self,instance,validated_data):
        validated_data.pop('created_by',None)
        return super().update(instance,validated_data)
    class Meta:
        model = Courses
        exclude = ['created_by','created_at','students']
        
        
# There are 2 methods to do it either uses hidden field which are not shown to the user or did not get data from the user
# and the other thing is we can add fields data directly in create



class enrolledCourse(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset = Courses.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True, default = serializers.CurrentUserDefault())
    def validate(self,validated_data):
        print(Enrolled.objects.filter(course = validated_data['course']).count(),validated_data['course'].seats)
        if Enrolled.objects.filter(course = validated_data['course']).count()>=validated_data['course'].seats:
            raise ValidationError('seats not available')
        return validated_data
    class Meta:
        model = Enrolled
        fields = ['course','user'] 
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Enrolled.objects.all(),
                fields=["user", "course"],
                message="You are already enrolled in this course."
            )
        ]
        
class studentDetailCourse(serializers.ModelSerializer):
    instructor = serializers.CharField(source = 'created_by.first_name')
    class Meta:
        model = Courses
        exclude = ['created_by','created_at','seats','students']
        
        
class instructorDetailCourse(serializers.ModelSerializer):
    class Meta:
        fields ='__all__'
        model = Courses
        


class ListCourses(serializers.ModelSerializer):
    
    class Meta:
        model = Courses 
        fields = ['title','description']
        
        
        
class assignmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__" 
        model = Assignments
        read_only_fields = ['subsection']
        
        
class listSubsection(serializers.ModelSerializer):
    assignments = assignmentSerializer(many=True)
    class Meta:
        fields = "__all__"
        model = Subsection   

        
class createSubsection(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    assignments = assignmentSerializer(many=True,read_only=True)
    class Meta:
        fields="__all__"
        model = Subsection