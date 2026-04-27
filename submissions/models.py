from django.db import models
from courses.models import Assignments
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Submissions(models.Model):
    assignment = models.ForeignKey(Assignments,on_delete = models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    file = models.FileField(upload_to = "submissions/")
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','assignment'],name='unique_user_assignment'
            )
        ]