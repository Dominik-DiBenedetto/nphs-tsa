from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('approve/', views.approve_users, name='approve_page'),
    path('deny/', views.deny_user, name='deny_user'),
    path('logout/', views.logout_view, name='logout'),
]