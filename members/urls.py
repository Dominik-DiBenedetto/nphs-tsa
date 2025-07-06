from django.urls import path

from . import views

urlpatterns = [
    path("", views.members_view, name="members"),
    path("attendance/", views.attendance_view, name="attendance"),
    path("attendance/add", views.add_attendance_record, name="add_attendance_record"),

]