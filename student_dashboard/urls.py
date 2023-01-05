from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("supplier/", views.supplierlist, name="supplier"),
    path("add_suppliers/", views.add_suppliers, name="add_supplier"),
    path("car_list/", views.cars, name="car_list"),
    path("costomers/", views.customers, name="customers"),
]
