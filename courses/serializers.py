from rest_framework import serializers
from .models import Courses, Enrolled, Subsection, Assignments
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class createCourse(serializers.ModelSerializer):
    def validate(self,kwargs):
        kwargs['created_by'] = self.context.get('request').user
        print(kwargs)
        print('cfndvbhvbvjnvjndivmfdvmf mdivfkim')
        return kwargs
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



class enrolledCourse(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset = Courses.objects.all())
    def validate_course(self,value):
        print(value.id)
        if Enrolled.objects.filter(course = value.id, user = self.context.get('request').user.id).exists():
            raise ValidationError("you are already enrolled in ths course.")
        return value
    def create(self,validate_data):
        print("validate_data:-",validate_data['course'])
        enroll = Enrolled(user= self.context.get("request").user,course = validate_data['course'])
        # print(enroll.user_id, enroll.course_id)
        enroll.save()
        print(enroll)
        return enroll
    def validate(self,validated_data):
        print(Enrolled.objects.filter(course = validated_data['course']).count(),validated_data['course'].seats)
        if Enrolled.objects.filter(course = validated_data['course']).count()>=validated_data['course'].seats:
            raise ValidationError('seats not available')
        return validated_data
    class Meta:
        fields = ['course'] 
        
        
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
        fileds = "__all__" 
        model = Assignments
        
        
class listSubsection(serializers.ModelSerializer):
    assignments = assignmentSerializer(many=True)
    class Meta:
        fields = "__all__"
        model = Subsection   
        
        
        
class createSubsection(serializers.ModelSerializer):
    
    def create(self,validated_data):
        print(self.context)
        validated_data['course'] = get_object_or_404(Courses,id = self.context.get('kwargs').get('course'))
        return super().create(validated_data)
    class Meta:
        exclude = ["course"]
        model = Subsection