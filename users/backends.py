from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model




class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('hello')
        user = super().authenticate(request,username,password,**kwargs)
        print(user)
        if user is None:
            return user
        if not user.is_instructor_approved:
            return None
        return user   
    
    
    
