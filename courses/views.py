from rest_framework.viewsets import ModelViewSet
from .models import Courses
from rest_framework.permissions import IsAuthenticated
from .permissions import isInstructor
from .serializers import createCourse, enrolledCourse
from rest_framework.decorators import action
from rest_framework.views import Response

class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user  
        if user.role =='student':
            return queryset.filter(students__id=user.id)
        elif user.role=='instructor':
            return queryset.filter(created_by__id=user.id)
        else:
            return queryset 
    def get_permissions(self):
        user = self.request.user 
        if self.action=="create":
            return [permission() for permission in self.permission_classes]+[isInstructor()]
        elif self.action=='enrolled':
            return [permission() for permission in self.permission_classes]
    def get_serializer_class(self):
        user = self.request.user
        if user.role =='instructor':
            return createCourse
        elif user.role=='student' and self.action=='enrolled':
            return enrolledCourse
    
    @action(detail=True)
    def enrolled(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors)
        
        
        

            
            
            