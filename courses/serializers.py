from rest_framework import serializers
from .models import Courses, Enrolled, Subsection, Assignments
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from courses import models
from django.db.models import Max
from django.utils import timezone


class createCourse(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["created_by"] = self.context.get("request").user
        return Courses.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("created_by", None)
        return super().update(instance, validated_data)

    def validate_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError("Seats must be greater than 0.")

        if self.instance:
            enrolled_count = self.instance.students.count()

            if value < enrolled_count:
                raise serializers.ValidationError(
                    f"Cannot reduce seats below " f"{enrolled_count} enrolled students."
                )

        return value

    class Meta:
        model = Courses
        fields = ["id", "title", "description", "seats"]


# There are 2 methods to do it either uses hidden field which are not shown to the user or did not get data from the user
# and the other thing is we can add fields data directly in create


class enrolledCourse(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Courses.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    def validate(self, validated_data):
        print(
            Enrolled.objects.filter(course=validated_data["course"]).count(),
            validated_data["course"].seats,
        )
        if (
            Enrolled.objects.filter(course=validated_data["course"]).count()
            >= validated_data["course"].seats
        ):
            raise ValidationError("seats not available")
        return validated_data

    class Meta:
        model = Enrolled
        fields = ["course", "user"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Enrolled.objects.all(),
                fields=["user", "course"],
                message="You are already enrolled in this course.",
            )
        ]


class studentDetailCourse(serializers.ModelSerializer):
    instructor = serializers.CharField(source="created_by.first_name")

    class Meta:
        model = Courses
        exclude = ["created_by", "created_at", "seats", "students"]


class instructorDetailCourse(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Courses


class ListCourses(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = ["title", "description"]


from rest_framework import serializers
from django.utils import timezone

from .models import Assignments


class assignmentSerializer(serializers.ModelSerializer):

    # incoming file from client
    uploaded_file = serializers.FileField(write_only=True)

    class Meta:
        model = Assignments

        fields = [
            "id",
            "title",
            "uploaded_file",
            "assignment_url",
            "file_name",
            "file_size",
            "deadline",
            "subsection",
            "is_archived",
        ]

        read_only_fields = [
            "subsection",
            "assignment_url",
            "file_name",
            "file_size",
            "is_archived",
        ]

    def validate_uploaded_file(self, value):

        # max 2MB
        if value.size > (2 * 1024 * 1024):
            raise serializers.ValidationError("File must be under 2 MB.")

        return value

    def validate_deadline(self, value):

        if value <= timezone.now():
            raise serializers.ValidationError("Deadline cannot be past.")

        return value

    def validate(self, attrs):

        subsection_id = self.context["kwargs"]["subsection"]

        title = attrs.get("title")

        qs = Assignments.objects.filter(
            subsection_id=subsection_id, title__iexact=title, is_archived=False
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                {"title": "Assignment title already exists."}
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop("uploaded_file", None)

        return Assignments.objects.create(**validated_data)


class listSubsection(serializers.ModelSerializer):
    assignments = assignmentSerializer(many=True)

    class Meta:
        fields = "__all__"
        model = Subsection


class createSubsection(serializers.ModelSerializer):

    # auto-generated if not sent
    order = serializers.IntegerField(required=False)

    course = serializers.PrimaryKeyRelatedField(read_only=True)

    assignments = assignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Subsection
        fields = "__all__"

    # Topic validation

    def validate_topic(self, value):

        if not value.strip():
            raise serializers.ValidationError("Topic cannot be blank.")

        if len(value.strip()) < 3:
            raise serializers.ValidationError("Topic too short.")

        return value

    # Order validation

    def validate_order(self, value):

        if value <= 0:
            raise serializers.ValidationError("Order must be positive.")

        return value

    # Cross-field validation

    def validate(self, attrs):

        course_id = self.context["kwargs"]["course"]

        topic = attrs.get("topic")

        order = attrs.get("order", None)

        # duplicate topic
        qs = Subsection.objects.filter(course_id=course_id, topic__iexact=topic)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError({"topic": "Topic already exists."})

        # duplicate order

        # only check if order supplied
        if order is not None:

            qs = Subsection.objects.filter(course_id=course_id, order=order)

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError({"order": "Order already used."})

        return attrs

    # Create subsection

    def create(self, validated_data):

        course = validated_data["course"]

        # auto assign order
        if validated_data.get("order") is None:

            last_order = course.subsections.aggregate(Max("order"))["order__max"]

            validated_data["order"] = (last_order or 0) + 1

        return super().create(validated_data)

    # Reorder safely on update
    @transaction.atomic
    def soft_delete(self, instance):

        old_order = instance.order

        has_assignments = instance.assignments.exists()
        if has_assignments:

            instance.is_archived = True
            instance.save()

        else:
            instance.delete()

        Subsection.objects.filter(
            course=instance.course, is_archived=False, order__gt=old_order
        ).update(order=models.F("order") - 1)

    @transaction.atomic
    def update(self, instance, validated_data):

        old_order = instance.order

        new_order = validated_data.get("order", old_order)

        if new_order != old_order:

            if new_order < old_order:

                Subsection.objects.filter(
                    course=instance.course, order__gte=new_order, order__lt=old_order
                ).update(order=models.F("order") + 1)

            else:

                Subsection.objects.filter(
                    course=instance.course, order__gt=old_order, order__lte=new_order
                ).update(order=models.F("order") - 1)

        return super().update(instance, validated_data)
