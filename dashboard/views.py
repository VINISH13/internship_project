from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendance, Task, Profile
from django.contrib.auth.models import User
from datetime import date
import json


# 🔥 Dashboard
@login_required
def dashboard(request):
    attendance = Attendance.objects.filter(user=request.user).order_by('date')

    dates = []
    status = []

    for i in attendance:
        dates.append(str(i.date))
        if i.status == "Present":
            status.append(1)
        else:
            status.append(0)

    context = {
        'dates': json.dumps(dates),
        'status': json.dumps(status)
    }

    return render(request, 'dashboard.html', context)


# 📅 Attendance Page
@login_required
def attendance_page(request):
    data = Attendance.objects.filter(user=request.user).order_by('-date')
    return render(request, 'attendance.html', {'data': data})


# 📝 TASK PAGE (KANBAN + DEADLINE)
@login_required
def task_page(request):
    todo = Task.objects.filter(user=request.user, status="Todo").order_by('-id')
    inprogress = Task.objects.filter(user=request.user, status="In Progress").order_by('-id')
    completed = Task.objects.filter(user=request.user, status="Completed").order_by('-id')

    return render(request, 'tasks.html', {
        'todo': todo,
        'inprogress': inprogress,
        'completed': completed,
        'today': date.today()   # 🔥 for deadline compare
    })


# 👤 Profile Page
@login_required
def profile_page(request):
    data = Profile.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {'data': data})


# 📅 Schedule
@login_required
def schedule_page(request):
    data = Attendance.objects.filter(user=request.user)
    return render(request, 'schedule.html', {'data': data})


# 📊 Report
@login_required
def report_page(request):
    total = Attendance.objects.filter(user=request.user).count()
    present = Attendance.objects.filter(user=request.user, status="Present").count()

    percent = 0
    if total > 0:
        percent = (present / total) * 100

    return render(request, 'report.html', {
        'total': total,
        'present': present,
        'percent': round(percent, 2)
    })


# 🔥 ADD TASK (ADMIN ONLY + DEADLINE)
@login_required
def add_task(request):

    if not request.user.is_superuser:
        return redirect('/tasks/')

    users = User.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_id = request.POST.get('user')
        deadline = request.POST.get('deadline')  # 🔥 NEW

        selected_user = User.objects.get(id=user_id)

        Task.objects.create(
            user=selected_user,
            title=title,
            description=description,
            deadline=deadline,   # 🔥 NEW
            status="Todo"
        )

        return redirect('/tasks/')

    return render(request, 'add_task.html', {'users': users})


# 🔥 UPDATE TASK STATUS
@login_required
def update_task_status(request, id, status):
    task = Task.objects.get(id=id)

    # 🔐 security
    if task.user != request.user:
        return redirect('/tasks/')

    task.status = status
    task.save()

    return redirect('/tasks/')