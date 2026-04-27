from django.db import models
from courses.models import Assignments
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


class Gradings(models.Model):
    assignment = models.ForeignKey(Assignments,on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    graded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user','assignment'],
                name = 'unique_user_assignment_gradings'
            )
        ]