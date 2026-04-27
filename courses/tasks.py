from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from courses.models import Assignments
from LearningManagementSystem.service.emailservice import send_email


@shared_task
def check_assignment_deadlines():

    now = timezone.now()

    # Only match assignments due 55–60 mins from now
    lower_bound = now + timedelta(minutes=0)
    upper_bound = now + timedelta(minutes=60)

    assignments = Assignments.objects.all()
    print(assignments)
    print('c djvdjvjvvv ')
    for assignment in assignments:

        students = assignment.subsection.course.students.all()

        for student in students:
            print("hello")
            send_email(
                to_email=student.email,
                subject="Assignment Reminder",
                body=f"""
Hello {student.first_name},

Your assignment for 
{assignment.subsection.course.title}

is due in less than one hour.
""" 
            )