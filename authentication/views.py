from django.shortcuts import render,redirect
from django.shortcuts import render
from django.views import View
from authentication.forms import PasswordResetForm, usersForm,RegitrationForm, UserUpdateForm
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import PasswordResetForm, SetPasswordForm, singleUserProfileForm
from django.db.models.query_utils import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('email/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder, Just in case you don\'t see the eamil')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

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
                try:
                    user = form.save(commit=False)
                    user.is_active = False
                    form.save()
                    activateEmail(request, user, form.cleaned_data.get('email'))
                except:
                    # activate the user if not sending the email
                    user = form.save(commit=False)
                    user.is_active = True
                    form.save()
                return redirect('/user-authentication/login/')
        else:
            form = RegitrationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('/student-dashboard/')


    
def profile(request, username):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Your profile has been updated!')
            return redirect("profile", user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(
            request=request,
            template_name="users/profile.html",
            context={"form": form}
            )
    
    return redirect("/student-dashboard/")

    from .forms import PasswordResetForm


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("email/reset_password_template.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        Password reset sent:
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('login/')

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("login")


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password/password_reset_confirm.html', {'form': form})

class userProfile(View):
    def get(self, request, *args, **kwargs):
        try:
            user_profile_instance = self.request.user.user_profile
        except:
            user_profile_instance= None
      
        update_form_user = usersForm(instance=self.request.user)
        update_form_user_profile = singleUserProfileForm(
            instance= user_profile_instance)
        context = {
            'user_form': update_form_user,
            'profile_form': update_form_user_profile
        }

        return render(request, template_name="student_dashboard_templates/student_profile.html", context=context)

    def post(self, request, *args, **kwargs):
        try:
            user_profile_instance = self.request.user.user_profile
        except:
            user_profile_instance  = None

        update_form_user = usersForm(
            self.request.POST or None,
            instance=self.request.user)
        update_form_user_profile = singleUserProfileForm(
            self.request.POST or None, self.request.FILES or None,
            instance= user_profile_instance)
        if update_form_user.is_valid() and update_form_user_profile.is_valid():
            user = update_form_user.save(True)
            profile = update_form_user_profile.save(False)
            if profile is None:
                profile.user = user
            profile.user = user
            profile.save()
            messages.success(
                self.request, ' your profile has been updated successfully')
            return redirect('userprofile')
        else:
            messages.warning(self.request, 'form is invalid')
        
            return redirect('userprofile')



