from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, request
from .forms import CourseForm, LessonForm
from django.shortcuts import get_object_or_404
from .models import Course, Enrollment, Lesson
from django.db.models import Q

@login_required
def createCourse(request):
    user = request.user
    if user.role != "TEACHER":
        return render(request, "403.html")
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect("courses:details", course_id=course.id)
    else:
        form = CourseForm()
    
    return render(request, "courses/course_form.html", {"form": form})

@login_required
def courseDetails(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    enrolled = False
    if request.user.is_authenticated and request.user.role == "STUDENT":
        enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    
        if request.method == "POST":
            if "enroll" in request.POST and not enrolled:
                Enrollment.objects.create(student=request.user, course=course)
                return redirect("courses:details", course_id=course.id)
            
            elif "unenroll" in request.POST and enrolled:
                Enrollment.objects.filter(student=request.user, course=course).delete()
                return redirect("courses:details", course_id=course.id)


    return render(request, "courses/course_details.html", {"course": course, "enrolled" : enrolled})

@login_required
def courseList(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")

    courses = Course.objects.all().order_by("-created_at")
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if category:
        courses = courses.filter(category=category)
    categories = Course.CATEGORY
    return render(request, "courses/course_list.html", {"courses": courses, "query":query, "category":category, "categories":categories})

@login_required
def myCourses(request):
    if request.user.role != "TEACHER":
        return render(request, "403.html")
    courses = Course.objects.filter(teacher=request.user).order_by("-created_at")
    return render(request, "courses/my_courses.html", {"courses": courses})

@login_required
def editCourse(request, course_id):
    course = get_object_or_404(Course, id = course_id)

    if request.user != course.teacher:
        return render(request, "403.html")
    
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:details', course.id)
    else:
        form = CourseForm(instance = course)
    return render(request, "courses/course_form.html", {"form": form, "edit_mode": True})

@login_required
def deleteCourse(request, course_id):
    course = get_object_or_404(Course, id = course_id)
    if request.user != course.teacher:
        return render(request, "403.html")
    if request == 'POST':
        course.delete() 
        return redirect('courses:my')
    return render(request, "courses/course_list.html", {"course":course})

@login_required
def addLesson(request, course_id):
    course = get_object_or_404(Course, id = course_id)
    lessons = course.lessons.all()

    if request.user != course.teacher and not request.user.is_superuser:
        return render(request, "403.html")
    
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect("courses:details", course_id)
    else:
        form = LessonForm()
    return render(request, "courses/lesson_form.html", {"form":form, "course":course})
        