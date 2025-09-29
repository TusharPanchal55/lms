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
    path('my/', views.myCourses, name = 'my')
]