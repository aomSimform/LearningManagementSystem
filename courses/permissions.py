from rest_framework.permissions import BasePermission


class isInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'instructor'


class isStudent(BasePermission):
    def has_permission(self,request,view):
        return request.user.role=='student'
    
    
    
class isCreatedByInstructor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role=='instructor':
            return obj.created_by == request.user
    
    
    
class isSubsectionCreatedByInstarctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("hellofdvbdhvdbv")
        print(request.user.id,obj.course.created_by.id)
        return request.user.id == obj.course.created_by.id