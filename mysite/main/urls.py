from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name=""),
    path("signup/", views.signup, name="signUpPage"),
    path("login/", views.login, name="loginPage"),
]
