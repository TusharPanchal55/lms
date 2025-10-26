from django.urls import path
from . import views
app_name = 'courses'
urlpatterns = [
    # path('', views.users, name = 'user'),
    path('', views.courseList, name = 'course_list'),
    path('create/', views.createCourse, name = 'create'),
    path('<int:course_id>/', views.courseDetails, name = 'details'),
    path('<int:course_id>/edit/', views.editCourse, name = 'edit'),
    path('<int:course_id>/delete', views.deleteCourse, name = 'delete'),
    path('<int:course_id>/add_lesson', views.addLesson, name = 'add_lesson'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll'),
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson, name='mark'),
    path('my/', views.myCourses, name = 'my'),
    path("lesson/<int:lesson_id>/quizzes/", views.quiz_list, name="quiz_list"),
    path("quiz/<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),

    path('course/<int:course_id>/quizzes/', views.teacher_quizzes, name='teacher_quizzes'),
    path('course/<int:course_id>/create-quiz/', views.create_quiz, name='create_quiz'),
    
    path('teacher/quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('teacher/question/<int:question_id>/add-answer/', views.add_answer, name='add_answer'),

    
]