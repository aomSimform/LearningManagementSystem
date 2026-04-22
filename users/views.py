from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, StudentProfile, InstructorProfile
from .serializers import UserSerializer
from rest_framework.response import Response
# Create your views here.

class registerViewSet(APIView):
    def post(self,request):
        user = UserSerializer(data  = request.data)
        user.is_valid(raise_exception=True)
        user.save()
        print(request.data)
        return Response(user.data,status=200)

        



