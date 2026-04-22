from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class role(models.TextChoices):
    STUDENT = 'student', 'Student'
    INSTRUCTOR = 'instructor','Instructor'

class User(AbstractUser):
    username = None 
    role = models.CharField(choices = role.choices,max_length = 10)
    email = models.EmailField(unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','role']
    
    
    
class StudentProfile(models.Model):
    user = models.OneToOneField('users.User',on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile/students/', null=True, blank=True)
    interests = models.TextField(blank=True)
    
    
    
class InstructorProfile(models.Model):
    user = models.OneToOneField('users.User',on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to = 'profile/instructors/', null=True, blank = True)
    expertise = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    qualification = models.CharField(max_length=200, blank=True)
    certifications = models.TextField(blank=True)