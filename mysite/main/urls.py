from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name=""),
    path("2/", views.index2, name=""),
    path("login/", views.login, name="loginPage"),
    path("signup/", views.signup, name="signUpPage"),
    path("registerInstructor/", views.registerInstructor, name="register"),
    path("registerStudent/", views.registerInstructor, name="register"),

]
