from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, template_name="intmain_home/index.html")
