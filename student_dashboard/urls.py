from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("topic_details/<slug>", views.topic_details, name="topic_details"),
]
