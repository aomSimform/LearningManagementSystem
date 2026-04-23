from rest_framework import serializers 
from .models import Courses, Enrolled



class createCourse(serializers.ModelSerializer):
    def validate(self,kwargs):
        kwargs['created_by'] = self.context.get('request').user
        print(kwargs)
        return kwargs
    def create(self,validated_data):
        validated_data['created_by']=self.context.get('request').user
        return Courses.objects.create(**validated_data)
    class Meta:
        model = Courses
        exclude = ['created_by','created_at','students']
        
        
# There are 2 methods to do it either uses hidden field which are not shown to the user or did not get data from the user
# and the other thing is we can add fields data directly in create



class enrolledCourse(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset = Courses.objects.all())
    def create(self,validate_data):
        validate_data = self.context.get("request").get("user")
        Enrolled.objects.create(user = validate_data['user'],course = validate_data['course'])
    class Meta:
        field = ['course']