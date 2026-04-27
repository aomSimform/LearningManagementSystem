from celery import shared_task  
from LearningManagementSystem.service.emailservice import send_email





@shared_task
def send_mail(user):
    message = f"Hello {user.get('first_name')} {user.get('last_name')} welcome to our site Thanks for registering."
    if user.get('role')=='instructor':
        message+=' you will get to use your profile after being accepted by admin.'
    print('email:-',user.get('email'))
    print('user:-',user)
    send_email(to_email=user.get('email'),subject='User Regristration',body=message)


@shared_task
def send_admin_mail(user):
    message = f"User with name:- {user.get('first_name')} {user.get('last_name')} has register as role:- {user.get('role')}"
    if user.get('role')=='instructor':
        message+='Accept it to make user registered.'
    send_email(to_email = 'kapadiaaom78@gmail.com',subject='User Regristration',body=message)




@shared_task
def send_instructor_approved_email(user):
    message='admin approves you for an instructor now you can use your profile'
    send_email(to_email=user['email'],subject='Permission Approved',body=message)
