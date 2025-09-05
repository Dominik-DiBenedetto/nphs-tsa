from django.urls import path

from . import views

urlpatterns = [
    path("portfolio_scanner/", views.portfolio_scanner, name="scan portfolio"),
    path("process_portfolio/", views.process_portfolio, name="process portfolio"),

]