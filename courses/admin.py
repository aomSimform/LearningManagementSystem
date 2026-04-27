<<<<<<< HEAD
from django.contrib import admin
from .models import Courses, Enrolled, Subsection, Assignments


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_by", "seats", "created_at")
    search_fields = ("title",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)   # newest courses first


@admin.register(Enrolled)
class EnrolledAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "enrolled_at")
    list_filter = ("enrolled_at",)
    ordering = ("-enrolled_at",)  # latest enrollments first


@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "course")
    search_fields = ("topic",)
    ordering = ("course", "topic")  # grouped by course, then alphabetical


# @admin.register(Assignments)
# class AssignmentsAdmin(admin.ModelAdmin):
#     list_display = ("id", "topic", "subsection")
=======
from django.contrib import admin
from .models import Courses, Enrolled, Subsection, Assignments


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_by", "seats", "created_at")
    search_fields = ("title",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)   # newest courses first


@admin.register(Enrolled)
class EnrolledAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "enrolled_at")
    list_filter = ("enrolled_at",)
    ordering = ("-enrolled_at",)  # latest enrollments first


@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "course")
    search_fields = ("topic",)
    ordering = ("course", "topic")  # grouped by course, then alphabetical


# @admin.register(Assignments)
# class AssignmentsAdmin(admin.ModelAdmin):
#     list_display = ("id", "topic", "subsection")
>>>>>>> fb2d2e087fc74deb708398fda7513f10b81ef9c2
#     ordering = ("subsection", "topic")