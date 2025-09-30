from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required



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
        return render(request, "users/student_db.html")
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