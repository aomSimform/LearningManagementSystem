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
        

        
        
        




