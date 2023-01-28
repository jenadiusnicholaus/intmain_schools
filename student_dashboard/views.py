from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from intmain_main_app.models import *


# Create your views here.

@login_required
def home(request):
    module = Module.objects.all()
    context = {
        'modules': module
    }
    return render(
        request, template_name = "student_dashboard_templates/home.html", context=context
    )
def topic_details(request, slug):
    topic_details = Topics.objects.get(slug = slug)
    context = {
            "topic_details":   topic_details
    }
    return render( request, template_name='student_dashboard_templates/activity.html', context=context)