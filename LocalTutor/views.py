from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse("Welcome to Local Tutor!")


def index(request):
    return render(request, 'main_app/index.html')


def home(request):
    return render(request, 'main_app/index.html')

def signup(request):
    return render(request, 'main_app/signup.html')

def login(request):
    return render(request, 'main_app/login.html')

def profile_setup(request):
    return render(request, 'main_app/profile_setup.html')

def search(request):
    return render(request, 'main_app/search.html')

