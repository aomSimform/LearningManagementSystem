<<<<<<< HEAD
from rest_framework.permissions import BasePermission


class isInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'instructor'


class isStudent(BasePermission):
    def has_permission(self,request,view):
        return request.user.role=='student'
    


class isCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
    
    
    
class isSubsectionCreatedByInstarctor(BasePermission):
    message='this subsection is not created by you'
    def has_object_permission(self, request, view, obj):
        print("hellofdvbdhvdbv")
        print(request.user.id,obj.course.created_by.id)
        return request.user.id == obj.course.created_by.id
    

class isAssignmentCretedByInstarctor(BasePermission):
    message = "you dont have access to this"
    def has_object_permission(self,request,view,obj):
        return obj.subsection.course.created_by==request.user
=======
from rest_framework.permissions import BasePermission


class isInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'instructor'


class isStudent(BasePermission):
    def has_permission(self,request,view):
        return request.user.role=='student'
    


class isCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
    
    
    
class isSubsectionCreatedByInstarctor(BasePermission):
    message='this subsection is not created by you'
    def has_object_permission(self, request, view, obj):
        print("hellofdvbdhvdbv")
        print(request.user.id,obj.course.created_by.id)
        return request.user.id == obj.course.created_by.id
    

class isAssignmentCretedByInstarctor(BasePermission):
    message = "you dont have access to this"
    def has_object_permission(self,request,view,obj):
        return obj.subsection.course.created_by==request.user
>>>>>>> fb2d2e087fc74deb708398fda7513f10b81ef9c2
        