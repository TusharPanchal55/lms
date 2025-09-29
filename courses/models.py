from django.db import models
from django.conf import settings


class Course(models.Model):
    CATEGORY = [
        ("PROG", "Programming"),
        ("DESIGN", "Designing"),
        ("AI", "Artificial Intelligence"),
        ("MATH", "Mathematics"),
        ("BUISNESS", "Buisness Communication"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "courses"
    )

    category = models.CharField(max_length=20, choices=CATEGORY)
    thumbnail = models.ImageField(upload_to="course_thumbnails/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
    
class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    video_file = models.FileField(upload_to='lecture/', blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title