from intmain_main_app.models import *

from django import forms

class CodeReviewForm(forms.Form):

    github_project_url = forms.CharField(required=True, widget= forms.URLInput(attrs={
        'class': 'form-control',
    }))
    descrition = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder':'Enter you content'
    }))
    have_other_source_of_ref = models.BooleanField(default=False)
    like_it = models.BooleanField(default=False)


    class Meta:
        model = CodeReviews
        fields = []