from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRoles(models.TextChoices):
    Student = 'student', 'Student'
    Instructor = 'instructor', 'Instructor'

class User(AbstractUser): 
    username = None 
    role = models.CharField(choices = UserRoles.choices, max_length=100)
    email = models.EmailField(unique = True)
    is_instructor_approved = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    def __str__(self):
        return self.first_name+" "+self.last_name
    
    @property
    def can_access_instructor_features(self):
        return (
            self.role == UserRoles.Instructor
            and self.approved
        )
    
    def save(self,*args,**kwargs):
        is_new = self.pk is None 
        if is_new and self.role==UserRoles.Student:
            self.approved = True
        super().save(*args,**kwargs)
        if is_new and self.role==UserRoles.Student:
            StudentProfile.objects.create(user=self)



    
class InstructorProfile(models.Model):
    user = models.OneToOneField('users.User',on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to = 'profile/instructors/', null=True, blank = True)
    expertise = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    qualification = models.TextField()
    
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile/students/', null=True, blank=True)
    interests = models.TextField()

    def __str__(self):
        return str(self.user)