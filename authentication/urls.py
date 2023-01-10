from django.contrib.auth import views
from django.urls import path
from . views import RegisterView,activate, password_reset_request,passwordResetConfirm

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout', ),
    path("register/", RegisterView.as_view(), name="register"),
    path("password_reset", password_reset_request, name="password_reset"),

    path('reset/<uidb64>/<token>/',passwordResetConfirm, name='password_reset_confirm'),
    path('reset/done/',views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    # acruvate the account
    path('activate/<uidb64>/<token>', activate, name='activate'),
 
  
]
