from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("home/", views.home, name="home"),
    path("sponsorships/", views.sponsorships, name="sponsorships"),
    path("sponsors/", views.sponsors, name="sponsors"),
    path("update_server/", views.update_server, name="update_server"),
]