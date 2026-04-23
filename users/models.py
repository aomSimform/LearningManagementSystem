from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserRoles(models.TextChoices):
    Student = 'student', 'Student'
    Instructor = 'instructor', 'Instructor'

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email or not password:
            raise ValueError('email and password are required')
        email = self.normalize_email(email)
        user = self.model(email = email,**extra_fields)
        
        user.set_password(password)
        user.full_clean()
        user.save(using = self._db)  #it means using same db model is using not new db.
        
        return user 
    
    
    
    def create_superuser(self,email,password,**extra_fields):
        if not email or not password:
            raise ValueError('email and password are required')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        
        user.is_superuser=True 
        user.is_staff = True
        user.full_clean()
        user.save(using = self._db)
        
        return user


class User(AbstractUser): 
    username = None 
    role = models.CharField(choices = UserRoles.choices, max_length=100, default=UserRoles.Student)
    email = models.EmailField(unique = True)
    last_name = models.CharField(max_length=100)
    is_instructor_approved = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    objects = UserManager()
    def __str__(self):
        return self.email
    
    def clean(self):
        super().clean()
        print("It is cleaned:-")
    @property
    def can_access_instructor_features(self):
        return (
            self.role == UserRoles.Instructor
            and self.approved
        )
    
    def save(self,*args,**kwargs):
        is_new = self.pk is None 
        if is_new and self.role==UserRoles.Student:
            self.is_instructor_approved = True 
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
    
    
    
    
    
    
    
    
    
    
