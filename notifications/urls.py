from django.urls import path
from . import views

urlpatterns = [
    path("save-subscription/", views.save_subscription, name="save_subscription"),
    path("send-test/", views.send_test_push, name="send_test_push"),
]
