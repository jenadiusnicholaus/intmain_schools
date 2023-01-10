from django.contrib.auth import views
from django.urls import path
from . views import RegisterView,activate

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout', ),
    path("register/", RegisterView.as_view(), name="register"),
    path('password_reset/done/',views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/',views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    # path("password_reset", password_reset_request, name="password_reset"),
    # acruvate the account
    path('activate/<uidb64>/<token>', activate, name='activate'),
 
  
]
