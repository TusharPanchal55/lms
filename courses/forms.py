from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Course, Lesson

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
