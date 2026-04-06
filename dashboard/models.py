from django.db import models
from django.contrib.auth.models import User


# 📅 Attendance
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)  # Present / Absent

    def __str__(self):
        return f"{self.user.username} - {self.date}"


# 📝 Task 
class Task(models.Model):

    STATUS_CHOICES = [
        ('Todo', 'Todo'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Todo'   # 🔥 default start
    )

    def __str__(self):
        return self.title


# 👤 Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    skills = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
