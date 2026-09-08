from django.urls import path
from . import views

urlpatterns = [
    # path("", views.view_base, name="base"),
    path("send_notification/", views.send_view, name="send_view"),

]
