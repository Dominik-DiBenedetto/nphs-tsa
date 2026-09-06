from django.urls import path

from . import views

urlpatterns = [
    path("", views.members_view, name="members"),
    path("<str:n_num>", views.view_member, name="view_member"),

    path("delete/", views.delete_member, name="delete_member"),
    path("update/", views.update_user, name="update_user"),
    path("strike/", views.give_strike, name="give_strike"),
    path("strike/remove/", views.remove_strike, name="remove_strike"),

    path("attendance/", views.attendance_view, name="attendance"),
    path("attendance/add", views.add_attendance_record, name="add_attendance_record"),
    path("attendance/scan", views.scan_attendance_record, name="scan_attendance"),
    path("attendance/delete/", views.delete_record, name="delete_record"),
    

]