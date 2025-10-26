from django.contrib import admin
from .models import Course, Enrollment, Lesson, Quiz, Question, Answer, StudentQuizAttempt


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



class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # show 4 blank option rows by default


    
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question")

admin.site.register(Answer, AnswerAdmin)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ("text", "quiz")
    search_fields = ("text", )

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "teacher", "created_at")  # ✅ now uses course and teacher
    search_fields = ("title", "course__title", "teacher__username")
    inlines = [QuestionInline]

@admin.register(StudentQuizAttempt)
class StudentQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "quiz", "score", "completed_at")
    search_fields = ("student__username", "quiz__title")
    readonly_fields = ("completed_at",)