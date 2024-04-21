import email
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views import View
import json 
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .utils import account_activation_token
# Create your views here.
    
class UsernameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry username is already taken'})
        return JsonResponse({'username_valid':True})
    
class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email:
            return JsonResponse({'email_error': 'Email is not valid'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry email in use, choose another'})
        return JsonResponse({'email_valid':True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'Authentication\Register.html')

    def post(self, request):
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            context = {
                'fieldValues': request.POST
            }
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "This password is too short. It must contain at least 6 characters.")
                    return render(request, 'Authentication\Register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
                link = reverse('activate', kwargs={'uidb64': email_body['uid'], 'token': email_body['token']})
                activate_url = 'http://' + current_site.domain + link
                email_subject = 'Activate your account'
                email_format = f'Welcome to WalletWatch, {user.username}!\n\n'
                email_format += 'Thank you for joining us. To activate your account, please click the following link:\n\n'
                email_format += f'{activate_url} \n'
                email_format += 'If you did not register on WalletWatch, please ignore this email.\n\n'
                email_format += 'Best regards,\n'
                email_format += 'The WalletWatch Team'
                
                send_mail(
                    email_subject,
                    email_format,
                    'noreply@gmail.com',
                    [email],
                    fail_silently=False
                )

                messages.success(request, "Account successfully created")
                return render(request, 'Authentication\Register.html')

        return render(request, 'Authentication\Register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)
            if not account_activation_token.check_token(user, token):
                return redirect('Login'+'?message'+'user is already activated')
            if user.is_active:
                return redirect('Login')
            user.is_active=True
            user.save()
            messages.success(request,'Account activated successfully')
            return redirect ('Login')
        except Exception as ex:
            pass
        return redirect(request, 'Login')
    
class LoginView(View):
    def get(self,request):
        return render(request,'Authentication/Login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +user.username+' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'Authentication/Login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'Authentication/Login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'Authentication/Login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('home')
    
