from django.contrib import admin
from .models import Course, Enrollment, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "thumbnail", "description", "teacher", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course")
    list_filter = ("student", "course")
    search_fields = ("student", "courses")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "video_file")
    list_filter = ("title", "content")
    search_fields = ("title", "content")
