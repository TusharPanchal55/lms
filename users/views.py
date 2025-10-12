from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from courses.models import Enrollment, Lesson, Progress, Course


def signUp(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/signup.html', {'form' : form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:db')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form' : form})

@login_required
def dashboard(request):
    user = request.user
    if user.role == "STUDENT":
        student = request.user
        enrollments = Enrollment.objects.filter(student=student).select_related('course')
        course_progress = []
        for e in enrollments:
            course = e.course
            tot_lessons = course.lessons.count()
            comp_lessons = Progress.objects.filter(
                student = student,
                lesson__course = course,
                completed = True
            ).count()
            progress = (comp_lessons / tot_lessons * 100) if tot_lessons > 0 else 0

            course_progress.append({
                'course' : course,
                'progress' : round(progress, 2),
                'comp_lessons' : comp_lessons,
                'tot_lessons' : tot_lessons,
            })
            context = {
                'student' : student,
                'course_progress' : course_progress,
            }
        return render(request, "users/student_db.html", context)
    elif user.role == "TEACHER":
        return render(request, "users/teacher_db.html")
    else:
        return redirect('users:login')

@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user_obj':request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form':form})