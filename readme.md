# Learning Management System (LMS)

A Django REST Framework based Learning Management System supporting:

- Authentication & Role-Based Access Control
- Courses Management
- Student Enrollments
- Ordered Course Subsections (Modules)
- Assignment Uploads via Cloudinary
- Submissions Module
- Grading Per Assignment
- Soft Deletes for Academic Data Preservation
- Notifications (planned integration)

---

# Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL / SQLite
- Cloudinary (Assignment File Storage)
- Celery + Redis (planned async tasks)

---

# Features

## Authentication & Roles

Roles:
- Instructor  
- Student  
- Admin (optional)

Permissions:
- Only instructors create/update/delete courses
- Only enrolled students access enrolled content
- Only instructors grade assignments
- Ownership checks prevent cross-course access

---

# Core Modules

## 1. Courses Module

### Instructors can:
- Create courses
- Update courses
- Delete/archive courses
- Manage subsections
- Create assignments
- Grade submissions

### Students can:
- Enroll in courses
- De-enroll from courses
- View enrolled courses
- Access subsections
- Submit assignments
- View grades

---

## 2. Enrollment Features

Implemented:

- Unique student-course enrollment
- Seat validation
- Prevent reducing seats below enrolled students
- Prevent over-enrollment
- Transaction-safe enrollment
- Row locking using `select_for_update()`
- Scoped throttling for enroll endpoint

Handles:
- Duplicate enroll requests
- Last-seat race conditions
- Seat overbooking

---

## 3. Subsections Module

Features:
- Ordered subsections/modules
- Auto-generated ordering
- Safe reordering logic
- Duplicate topic prevention
- Duplicate order prevention
- Soft delete when dependencies exist
- Order re-sequencing after deletion

---

## 4. Assignments Module

Features:
- Assignment creation and deletion
- File upload to Cloudinary
- Stores Cloudinary secure URL
- File size limited to 2 MB
- Deadline validation
- Duplicate assignment title prevention
- Soft delete if submissions exist

Assignment metadata stored:

- assignment_url  
- file_name  
- file_size  
- deadline

---

## 5. Submissions Module

Features:
- Students submit assignment work
- Submission linked to assignment + student
- Supports submission tracking
- Prevent duplicate submission rules (if configured)
- Late submission handling (optional)

---

## 6. Grading Module (Per Assignment)

Features:
- Grade per submitted assignment
- Instructor-only grading access
- One grade linked to a submission
- Grade retrieval for students
- Grade history can be extended later

Supports:
- Numeric scores
- Feedback/comments
- Grade visibility to student

Workflow:

Course  
→ Subsection  
→ Assignment  
→ Student Submission  
→ Instructor Grade

---

# API Endpoints

Base:

```http
http://127.0.0.1:8000/
```

---

## Courses

### List Courses

```http
GET /courses/
```

### Create Course

```http
POST /courses/
```

### Course Detail

```http
GET /courses/<id>/
```

### Update Course

```http
PATCH /courses/<id>/
```

### Delete Course

```http
DELETE /courses/<id>/
```

---

## Enrollment

### Enroll

```http
POST /courses/<id>/enroll/
```

### De-enroll

```http
DELETE /courses/<id>/deenroll/
```

---

## Subsections

### List Subsections

```http
GET /courses/<course_id>/subsections/
```

### Create Subsection

```http
POST /courses/<course_id>/subsections/
```

### Update Subsection

```http
PATCH /courses/<course_id>/subsections/<subsection_id>/
```

### Delete Subsection

```http
DELETE /courses/<course_id>/subsections/<subsection_id>/
```

---

## Assignments

### Create Assignment

```http
POST /courses/<course_id>/subsections/<subsection_id>/assignments/
```

Use `multipart/form-data`

Fields:

```text
title
deadline
uploaded_file
```

---

### Delete Assignment

```http
DELETE /courses/<course_id>/subsections/<subsection_id>/assignments/<id>/
```

---

## Submissions

### Submit Assignment

```http
POST /assignments/<assignment_id>/submit/
```

### View Submission

```http
GET /assignments/<assignment_id>/submission/
```

---

## Grading

### Grade Submission

```http
POST /submissions/<submission_id>/grade/
```

### Update Grade

```http
PATCH /submissions/<submission_id>/grade/
```

### View Grade

```http
GET /submissions/<submission_id>/grade/
```

---

# URL Configuration

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CoursesViewSet,
    SubSectionViewSet,
    AssignmentsCreateDeleteView
)

router = DefaultRouter()

router.register(
    r'courses',
    CoursesViewSet,
    basename='courses'
)

urlpatterns = [

    path(
        '',
        include(router.urls)
    ),

    path(
        'courses/<int:course>/subsections/',
        SubSectionViewSet.as_view({
            'get':'list',
            'post':'create'
        })
    ),

    path(
        'courses/<int:course>/subsections/<int:pk>/',
        SubSectionViewSet.as_view({
            'patch':'partial_update',
            'delete':'destroy'
        })
    ),

    path(
        'courses/<int:course>/subsections/<int:subsection>/assignments/',
        AssignmentsCreateDeleteView.as_view()
    ),

    path(
        'courses/<int:course>/subsections/<int:subsection>/assignments/<int:pk>/',
        AssignmentsCreateDeleteView.as_view()
    ),
]
```

---

# Security & Validation

Implemented protections against:

- IDOR attacks
- Nested route mismatches
- Duplicate enrollments
- Enrollment race conditions
- Duplicate subsection ordering
- File upload abuse
- Archived object modification
- Unauthorized grading access

---

# Future Improvements

Planned:

- Quiz engine
- Certificates
- Discussion forums
- Calendar integration
- Background jobs with Celery
- Plagiarism detection
- SCORM/LTI support

---

# Run Project

```bash
git clone <repo>
cd LearningManagementSystem

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

---

# Author

Aom Kapadia