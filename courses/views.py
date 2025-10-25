from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, request
from .forms import CourseForm, LessonForm
from django.shortcuts import get_object_or_404
from .models import Course, Enrollment, Lesson, Progress, Quiz, Question, Answer, StudentQuizAttempt
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

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
    lessons = course.lessons.all()
    

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
    completed_lessons = []
    if request.user.is_authenticated:
        completed_lessons = Progress.objects.filter(
            student = request.user,
            completed = True
        ).values_list('lesson_id', flat=True)
    return render(request, "courses/course_details.html", {'course':course, 'lessons':lessons, 'completed_lessons':completed_lessons, 'enrolled':enrolled})

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

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id = course_id)
    if request.user.role != 'STUDENT':
        messages.error(request, "Only Students can enroll!")
        return redirect('courses:details', course_id=course.id)
    
    if request.method == 'POST':
        if "enroll" in request.POST:
            enrollment, created = Enrollment.objects.get_or_create(
            student = request.user,
            course = course
            )

            if created:
                messages.success(request, "You have enrolled Successfully!")
            else:
                messages.info(request, "You have already enrolled for the course")
        elif "unenroll" in request.POST:
            Enrollment.objects.filter(student=request.user, course=course).delete()
            messages.warning(request, "You have unenrolled from this course.")
        
    return redirect('courses:details', course_id = course.id)

@login_required
def mark_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id = lesson_id)
    course = lesson.course
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, "You must enroll for the course first!")
        return redirect('courses:details', course_id=course.id)
    progress, created = Progress.objects.get_or_create(
        student = request.user,
        lesson = lesson
    )
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()

    messages.success(request, f"Lesson Completed! '{lesson.title}'")
    return redirect('courses:details', course_id=course.id)


@login_required
def quiz_list(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quizzes = Quiz.objects.filter(lesson=lesson)
    return render(request, "courses/quiz_list.html", {"lesson": lesson, "quizzes": quizzes})




@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    

    if request.method == "POST":
        score = 0
        results = []

        for question in questions:
            selected_answer_id = request.POST.get(f"question_{question.id}")
            correct_answer = question.answers.filter(is_correct=True).first()

            if selected_answer_id:
                answer = Answer.objects.get(id=selected_answer_id)
                is_correct = answer.is_correct
            else:
                is_correct = False

            if is_correct:
                score += 1

            results.append({
                'question': question.text,
                'selected': answer.text if selected_answer_id else None,
                'correct': correct_answer.text,
                'is_correct': is_correct
            })

        percentage = round((score / questions.count()) * 100, 2)

        # Graded message
        if percentage >= 90:
            grade_msg = "Excellent!"
        elif percentage >= 70:
            grade_msg = "Good Job!"
        elif percentage >= 50:
            grade_msg = "Needs Improvement"
        else:
            grade_msg = "Better Luck Next Time"

        attempt, created = StudentQuizAttempt.objects.get_or_create(
            student=request.user,
            quiz=quiz,
            defaults={'score': score}
        )
        if not created:
            attempt.score = score
            attempt.save()

        return render(request, 'courses/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'percentage': percentage,
            'grade_msg': grade_msg,
            'results': results
        })

    return render(request, 'courses/take_quiz.html', {'quiz': quiz, 'questions': questions})
