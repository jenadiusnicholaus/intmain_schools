from django.shortcuts import render,redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from authentication.forms import RegitrationForm
from django.contrib import messages


# Sign Up View
class RegisterView(View):
    
    def get(self, request,*args, **kwargs ):
        form = RegitrationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

    def post(self, request,*args, **kwargs ):
        if request.method == 'POST':
            form = RegitrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/user-authentication/login/')
        else:
            form = RegitrationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)
    