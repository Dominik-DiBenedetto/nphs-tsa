from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("event/<int:event_id>/", views.view_event, name="event"),
    path("matchmaker/", views.event_matchmaker, name="Event Matchmaker"),
]