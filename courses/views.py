from rest_framework.viewsets import ModelViewSet
from .models import Courses, Subsection
from rest_framework.permissions import IsAuthenticated
from .permissions import isInstructor, isStudent, isCreatedByInstructor, isSubsectionCreatedByInstarctor
from .serializers import createCourse, enrolledCourse, ListCourses, studentDetailCourse, instructorDetailCourse, listSubsection, createSubsection
from rest_framework.decorators import action
from rest_framework.views import Response
from .filtersbackends import SubsectionFilter
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound


class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user  
        if user.role =='student':   
            return queryset.filter(students__id=user.id).distinct()
        elif user.role=='instructor':
            return queryset.filter(created_by__id=user.id)
        else: 
            return queryset 
    def get_permissions(self):
        user = self.request.user 
        if self.action=="create" or self.action=="destroy" or self.action=="partial_update":
            return [permission() for permission in self.permission_classes]+[isInstructor()]
        elif self.action=='enrolled':
            return [permission() for permission in self.permission_classes]+[isStudent()]
        elif self.action=='retrieve' and user.role=='instructor':
            return [permission() for permission in self.permission_classes]+[isCreatedByInstructor()]
        return [permission() for permission in self.permission_classes]
    def get_serializer_class(self):
        user = self.request.user
        if self.action=='create' or self.action=="partial_update":
            return createCourse
        elif self.action=='enrolled':
            return enrolledCourse
        elif self.action=='list':
            return ListCourses
        elif self.action=='retrieve':
            if self.request.user.role=='student':
                return studentDetailCourse
            return instructorDetailCourse
            
    def destroy(self,request, *args, **kwargs):
        res = super().destroy(request,*args,**kwargs)
        if res.status_code==204:
            return Response({"success":f"course with id {kwargs['pk']} gets deleted successfully"})
        return res
    @action(detail=True)
    def enrolled(self,request,*args,**kwargs):
        print('hello I am at the enrolled view')
        print(request.data)
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success':"you enrolled successfully to course"},status=200)
        return Response(serializer.errors)
        
        
        

            
            
class SubSectionViewSet(ModelViewSet):
    queryset = Subsection.objects.all().prefetch_related('assignments')
    filter_backends=[SubsectionFilter] 
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action=='list':
            return listSubsection
        elif self.action=="create" or self.action=="partial_update":
            return createSubsection
    def get_queryset(self):
        course = Subsection.objects.filter(course = self.kwargs['course'])
        if not course.exists():
            raise NotFound("course id is invalid")
        queryset = super().get_queryset()
        if self.request.user.role=='student':
            return queryset.filter(course__students__id = self.request.user.id)
        else:
            print(queryset.filter(course__created_by = self.request.user.id).values, self.request.user.id)
            return queryset
    def get_permissions(self):
        if self.action =='create' or self.action=='partial_update' or self.action=='destroy':
            return [permission() for permission in self.permission_classes]+[isInstructor(),isSubsectionCreatedByInstarctor()]
        return super().get_permissions()
    
    def get_serializer_context(self):
        context =  super().get_serializer_context()         
        context['kwargs'] = self.kwargs 
        return context
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs) 
        return Response({"success":f"object with id:- {kwargs['pk']} gets deleted successfully"})
    
    
