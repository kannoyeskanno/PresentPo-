from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib import messages



# Create your views here.

def index(response):
	return render(response,  "main/base.html", {})

def signup(response):
	return render(response, "main/signup.html", {})

def login(request):
	if request.method == "POST":
		usename = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=usename, password=password)
		if user is not None:
			login(user)
			return redirect("main/signup.html")
		else:
			messages.success(request, ("There was an error"))
			return redirect("main/login.html")
	else:
		return render(request, "main/login.html", {})


def registerInstructor(request):
	if request.method == "POST":
		usename = request.POST['username']
		password = request.POST['password']
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(request, "main/instructorRegister.html", {})
	else:
		form = UserCreationForm()
	return render(request, "main/instructorRegister.html", {})

def registerStudent(response):
	return render(response, "main/studentRegister.html", {})



