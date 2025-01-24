from django.urls import path
from . import views

app_name = "register"

urlpatterns = [
    path("", views.register, name="register"),  # Handles /register/
    path("", views.login_view, name="login"),  # Login URL
]