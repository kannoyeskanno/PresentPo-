from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(response):
	return render(response,  "main/base.html", {})

def signup(response):
	return render(response, "main/signup.html", {})


def login(response):
	return render(response, "main/login.html", {})

def registerInstructor(response):
	return render(response, "main/instructorRegister.html", {})

def registerStudent(response):
	return render(response, "main/studentRegister.html", {})





#
# def index(response):
# 	return HttpResponse("<h1>aaaaa</h1>")
# def signUp(response):
# 	return HttpResponse("<h1>signusadasd</h1>")
#
#
#
