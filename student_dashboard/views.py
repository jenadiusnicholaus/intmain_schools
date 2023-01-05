from django.shortcuts import render

# Create your views here.


def home(request):
    context = {}
    return render(
        request, template_name="student_dashboard_templates/home.html", context=context
    )


def login(request):
    context = {}
    return render(request, template_name="student_dashboard_templates/login.html")


def register(request):
    context = {}
    return render(request, template_name="student_dashboard_templates/register.html")


def supplierlist(request):
    context = {}
    return render(request, template_name="student_dashboard_templates/supplier.html")


def add_suppliers(request):
    return render(
        request, template_name="student_dashboard_templates/add_supplier.html"
    )


def cars(request):
    return render(request, template_name="student_dashboard_templates/cars.html")


def add_cars(request):
    return render(request, template_name="student_dashboard_templates/add_car.html")


def add_cars(request):
    return render(request, template_name="student_dashboard_templates/add_car.html")


def customers(request):
    return render(request, template_name="student_dashboard_templates/customers.html")
