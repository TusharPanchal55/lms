from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    # path('', views.users, name = 'user'),
    path('signup/', views.signUp, name = 'signup'),
    path('', views.login_view, name = 'login'),
    path('dashboard/', views.dashboard, name = 'db'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name = 'profile'),
    path('profile/edit/', views.profile_edit, name = 'profile_edit')
]