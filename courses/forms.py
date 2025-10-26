from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Course, Lesson
from django import forms
from .models import Quiz, Question, Answer

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category','thumbnail']
        widgets = {
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows' : 4}),
            'video_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']



