from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Enrolled(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey("Courses", on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_user_course"
            )
        ]


class Courses(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructors",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    seats = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    students = models.ManyToManyField(
        "users.User", through=Enrolled, related_name="courses"
    )
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # def enroll_student(self,user_id):
    #     Enrolled.objects.create(user = user_id, course = self)


from django.db import models


class Subsection(models.Model):

    course = models.ForeignKey(
        "Courses", on_delete=models.CASCADE, related_name="subsections"
    )

    topic = models.CharField(max_length=300)

    description = models.TextField()

    order = models.PositiveIntegerField()

    is_archived = models.BooleanField(default=False)

    class Meta:

        ordering = ["order"]

        constraints = [
            # Prevent duplicate topics in same course
            models.UniqueConstraint(
                fields=["course", "topic"], name="unique_topic_per_course"
            ),
            # Prevent duplicate order numbers
            models.UniqueConstraint(
                fields=["course", "order"], name="unique_order_per_course"
            ),
        ]

    def __str__(self):
        return self.topic


class Assignments(models.Model):

    subsection = models.ForeignKey(
        "Subsection", on_delete=models.CASCADE, related_name="assignments"
    )

    title = models.CharField(max_length=255)

    assignment_url = models.URLField(null=True, blank=True)

    file_name = models.CharField(max_length=255, null=True, blank=True)

    file_size = models.PositiveIntegerField(null=True, blank=True)

    deadline = models.DateTimeField()

    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title
