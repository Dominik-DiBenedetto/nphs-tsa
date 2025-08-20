from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("event/<int:event_id>/", views.view_event, name="event"),
    path("event/<int:event_id>/delete", views.delete_event, name="delete_event"),
    path("event/<int:event_id>/update/", views.update_event, name="update_event"),
    path('events/<int:event_id>/ceg/', views.view_ceg_file, name='view_ceg'),
    path("add_event/", views.add_event, name="add_event"),
    path("matchmaker/", views.event_matchmaker, name="Event Matchmaker"),
]