from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView, LoginView,LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.urls import path


urlpatterns = [
    path('register',RegistrationView.as_view(), name="register"),
    path('Login',LoginView.as_view(), name="Login"),
    path('Logout',LogoutView.as_view(), name="Logout"),
    path('validate_username',csrf_exempt(UsernameValidationView.as_view()),name='validate_username'),
    path('validate_email',csrf_exempt(EmailValidationView.as_view()),name='validate_email'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name="activate"),
]

