from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
    
    role = models.CharField(
        max_length = 20,
        choices = Role.choices,
        default = Role.STUDENT
    )

# Create your models here.
