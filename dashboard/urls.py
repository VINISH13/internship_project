from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance_page, name='attendance'),
    path('tasks/', views.task_page, name='tasks'),
    path('profile/', views.profile_page, name='profile'),
    path('schedule/', views.schedule_page),
    path('report/', views.report_page),
    path('add-task/', views.add_task, name='add_task'),path('update-task/<int:id>/<str:status>/', views.update_task_status, name='update_task'),
]