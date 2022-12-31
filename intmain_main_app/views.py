from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, template_name="intmain_home/intmain_home_page_index.html")
