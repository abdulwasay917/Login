from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, ForgotPasswordForm
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.forms import SetPasswordForm




def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Email already exists'
                })

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            try:
                usern = User.objects.get(username=identifier).username
            except User.DoesNotExist:
                    try:
                        usern = User.objects.get(email=identifier).username
                    except User.DoesNotExist:
                        return render(request, 'login.html', {
                            'form': form,
                            'error': 'Invalid email'
                        })

            user = authenticate(request, username=usern, password=password)

            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Invalid password'
                })
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def forgot_password(request):
    if request.method == "POST":
        error = None
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
                message = f"Click this link to reset your password: {link}"
                send_mail('Reset Your Password',
                message,
                settings.EMAIL_HOST_USER ,
                [user.email],
                fail_silently=False,)
                return render(request,'successful.html')
            else:
                error = "user or his email does not exist"
    else:
        form = ForgotPasswordForm()
        error=None
    return render(request, 'forgot.html', {'form': form, 'error':error})

def reset_password(request, uidb64, token):
    user_model = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_model.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'resetpassword.html', {'form': form})
    else:
        return render(request, 'reset_password_invalid.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')
