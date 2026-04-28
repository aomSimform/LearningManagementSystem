from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, StudentProfile, InstructorProfile
from .serializers import UserCreationSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.db import transaction 
from users.tasks import send_mail, send_admin_mail
from rest_framework import viewsets, mixins, generics
from .serializers import StudentProfileSerailizers, InstructorProfileSerializers
from .permissions import isProfileUser
USER = get_user_model()
# Create your views here.

class registerViewSet(APIView):
    def post(self,request):
        user = UserCreationSerializer(data  = request.data)
        if user.is_valid():
            user.save()
            print(user.data)
            print('hekfomevk')
            transaction.on_commit(lambda:send_mail.delay(user.data))
            transaction.on_commit(lambda:send_admin_mail.delay(user.data))
            print(request.data)
            return Response(user.data,status=200)
        return Response(user.errors,status=400) 
    
    
class LoginViewSet(APIView):
    def post(self,request):
        
        user = UserLoginSerializer(data = request.data)
        
        if not user.is_valid():
            return Response(user.errors, status = 400)
        
        user = USER.objects.get(email = request.data.get('email'))
        refresh = RefreshToken.for_user(user)
        return Response(data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        

        
        
        




class ProfileViewset(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.role =='student':
            return StudentProfileSerailizers 
        return InstructorProfileSerializers
    
    def get_object(self):
        user = self.request.user
        if user.role == "student":
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            return profile
        profile, _ = InstructorProfile.objects.get_or_create(user=user)
        return profile
