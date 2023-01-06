from django.shortcuts import render

# Create your views here.

def login(request):
    context = {}
    return render(request, template_name="authentication/login.html")


def register(request):
    context = {}
    return render(request, template_name="authentication/register.html")