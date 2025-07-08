from django.urls import path

from . import views

urlpatterns = [
    path("", views.achievements_view, name="index"),
    path("add_conference/", views.add_conference, name="add_conference"),
    path("add_achievement/", views.add_achievement, name="add_achievement"),
    path("get_achievements/", views.get_achievements, name="get_achievements"),

]