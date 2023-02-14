from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from intmain_main_app.models import *
from . forms import CodeReviewForm


# Create your views here.

@login_required
def home(request):
    module = Module.objects.all()
    code_review =  CodeReviewForm()
    context = {
        'code_review_form': code_review,
        'modules': module
    }
    return render(
        request, template_name = "student_dashboard_templates/home.html", context=context
    )

@login_required
def topic_details(request, slug):
    topic_details = Topics.objects.get(slug = slug)
    context = {
            "topic_details":   topic_details
    }
    return render( request, template_name='student_dashboard_templates/activity.html', context=context)

@login_required
def post_code_reviews(request):
    pass