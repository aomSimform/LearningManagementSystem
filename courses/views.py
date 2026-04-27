from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, generics
from .models import Courses, Subsection, Enrolled, Assignments
from rest_framework.permissions import IsAuthenticated
from .permissions import isInstructor, isStudent, isCourseOwner, isSubsectionCreatedByInstarctor, isAssignmentCretedByInstarctor
from .serializers import createCourse, enrolledCourse, ListCourses, studentDetailCourse, instructorDetailCourse, listSubsection, createSubsection, assignmentSerializer
from rest_framework.decorators import action
from rest_framework.views import Response
from .filtersbackends import SubsectionFilter
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, NotFound 

class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        queryset = super().get_queryset()
        print('hello')
        user = self.request.user  
        if self.action=="list":
            if self.request.user.role=='student':
                queryset = queryset.filter(students=self.request.user)
            else:
                queryset = queryset.filter(created_by=self.request.user)
        return queryset
    def get_permissions(self):
        user = self.request.user 
        if self.action in ["create","partial_update","destroy"]:
            return [permission() for permission in self.permission_classes]+[isInstructor()]
        elif self.action=='retrieve' and user.role=='instructor':
            return [permission() for permission in self.permission_classes]+[isCourseOwner()]
        elif self.action in ['enrolled','deenrolled']:
            return [permission() for permission in self.permission_classes]+[isStudent()]
        return [permission() for permission in self.permission_classes]
    def get_serializer_class(self):
        user = self.request.user
        if self.action in ["create","partial_update"]:
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
            return Response({"success":f"course with id {kwargs['pk']} gets deleted successfully"},status=204)
        return res
    @action(detail=True)
    def enrolled(self,request,*args,**kwargs):
        print('hello I am at the enrolled view')
        serializer = self.get_serializer(data={'course':kwargs['pk']})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response({'success':"you enrolled successfully to course"},status=200)
        return Response(serializer.errors)
    
    @action(detail=True)
    def deenrolled(self,request,*args,**kwargs):
        print("I am de enrolling from this course")
        print(request.data)
        is_enrolled = Enrolled.objects.filter(course = kwargs['pk'],user = self.request.user)
        if is_enrolled.exists():
            is_enrolled.delete()
            return Response({"success":"de enrolled successfully"})
        return Response({"error":"you are not enrolled in this course"},status=400)

        
        
        

            
            
class SubSectionViewSet(ModelViewSet):
    queryset = Subsection.objects.all().prefetch_related('assignments')
    permission_classes = [IsAuthenticated]
    serializer_class = createSubsection

    def get_queryset(self):
        course = self.get_course()
        if self.action=='list':
            return super().get_queryset().filter(course = course)
        return super().get_queryset().filter(course=self.kwargs.get("course"))
    def get_permissions(self):
        if self.action in ['create','partial_update','destroy']:
            return [permission() for permission in self.permission_classes]+[isInstructor(),isSubsectionCreatedByInstarctor()]
        return super().get_permissions()
    
    def get_serializer_context(self):
        context =  super().get_serializer_context()         
        context['kwargs'] = self.kwargs 
        return context
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs) 
        return Response({"success":f"object with id:- {kwargs['pk']} gets deleted successfully"})
    def perform_create(self,serializer):
        return serializer.save(course=self.get_course())

    def get_course(self):
        course_id = self.kwargs["course"]

        try:
            course = Courses.objects.get(pk=course_id)
        except Courses.DoesNotExist:
            raise NotFound("Course does not exist.")

        if self.request.user.role == "student":
            if not course.students.filter(pk=self.request.user.pk).exists():
                raise PermissionDenied(
                    "You are not enrolled in this course."
                )

        else:
            if course.created_by != self.request.user:
                raise PermissionDenied(
                    "You do not have permission to modify this course."
                )

        return course
    



    



class AssignmentsCreateDeleteView(mixins.CreateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    permission_classes = [isInstructor, isAssignmentCretedByInstarctor]
    serializer_class = assignmentSerializer
    queryset = Assignments.objects.all()

    def get_subsection(self):
        try:
            print(self.kwargs.get("subsection"))
            subsection = get_object_or_404(Subsection,pk = self.kwargs.get('subsection'))
            print(self.kwargs.get("subsection"))
        except:
            raise NotFound("subsecton does not exists")
        
        if subsection.course.created_by != self.request.user:
            raise PermissionDenied("you dont have permission to access this course")
        print('cnedvnuvnuvn')
        return subsection


    def post(self, request, *args, **kwargs):
        print('post hit')
        print(request.data)
        return self.create(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        print(self.kwargs)
        res =  self.destroy(request, *args, **kwargs)
        return Response({"success":f"assignmnet with id:- {kwargs['pk']} gets deleted successfully"})
    def perform_create(self,serializer):
        print('operform create hit'+"mncdnvn",self.get_subsection())
        return serializer.save(subsection = self.get_subsection())

    
