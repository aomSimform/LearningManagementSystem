from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Enrolled(models.Model):
    user = models.ForeignKey('users.User',on_delete=models.CASCADE)
    course = models.ForeignKey('Courses',on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add = True)
    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['user','course'],name='unique_user_course'
            )
        ]
class Courses(models.Model):
    title = models.CharField(max_length=300,unique=True)
    description = models.TextField()
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank = True,related_name = 'instructors')
    created_at = models.DateTimeField(auto_now_add = True)
    seats = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(200)])
    students = models.ManyToManyField('users.User',through = Enrolled,related_name = 'courses')
    def __str__(self):  
        return self.title
    # def enroll_student(self,user_id):
    #     Enrolled.objects.create(user = user_id, course = self)
class Subsection(models.Model):
    course = models.ForeignKey('Courses',on_delete=models.CASCADE,related_name='subsections')
    topic = models.CharField(max_length=300)
    description = models.TextField()
    
    def __str__(self):
        return self.topic
    
class Assignments(models.Model):
    subsection = models.ForeignKey('Subsection',on_delete = models.CASCADE,related_name = 'assignments')
    file = models.FileField(upload_to = 'assignments/')
    deadline = models.DateTimeField()
    user=models.ManyToManyField('users.User',through = 'submissions.Submissions',related_name = 'submitted_assignments')
    grades = models.ManyToManyField('users.User',through = 'grading.Gradings',related_name = 'assignments_grades')
    
    def __str__(self):
        return self.topic
    
    