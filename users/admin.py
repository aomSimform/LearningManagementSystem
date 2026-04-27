from django.contrib import admin
from .models import User, StudentProfile, InstructorProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .tasks import send_instructor_approved_email
# Register your models here.


admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    ordering = ['email']
    
    list_display = (
        "email",
        "role",
        "is_instructor_approved"
    )

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        if change:

            old_user = User.objects.get(pk=obj.pk)

            was_unapproved = (
                old_user.is_instructor_approved is False
            )

        else:
            was_unapproved = False


        super().save_model(
            request,
            obj,
            form,
            change
        )


        if (
            change and
            was_unapproved and
            obj.is_instructor_approved
        ):
            send_instructor_approved_email.delay({'id':obj.id,'first_name':obj.first_name,'last_name':obj.last_name,'email':obj.email})