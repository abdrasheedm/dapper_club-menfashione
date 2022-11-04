from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Account
from .forms import RegistrationForm

#  verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# mobile_otp
from .otp_verification import *


# Create your views here.

def register(request):

    if 'email' in request.session:
        return redirect('index')

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, phone_number=phone_number, password=password)
            user.save()

            # user activation
            # verification_user = sent_otp(phone_number, user)
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            messaage = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                # 'phone_number' : phone_number,
                # 'uid' : user.pk,
                # 'verification_user' : verification_user,
            })
            to_mail = email
            send_male = EmailMessage(mail_subject, messaage, to=[to_mail])
            send_male.send()
            
            messages.success(request, "Activation email is sent to your email. Please activate your account")
            return redirect('register')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)



def activate_email(request,uidb64, token):

    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account.objects.get(pk=uid) 

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        user_verifcation=VerificationUser()
        user_verifcation.user=user
        user_verifcation.email_verification=True
        user_verifcation.save()
        messages.success(request, 'Account registered succesfully. Please to signin...')
        return redirect('signin')
    else:
        messages.error(request, 'Link expired! Please try again ..')
        return redirect('register')



def signin(request):

    if 'email' in request.session:
        return redirect('index')

    form = RegistrationForm()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password = password )
        if user is not None:
            request.session['id'] = user.pk
            print(user.pk)
            login(request, user)
            messages.success(request, "Logged in Succesfully")
            return redirect('index')

        else:
            messages.error(request, "Invalid login credentials")

    
    context = {'form':form}
    return render(request, 'accounts/signin.html', context)

@login_required(login_url='signin')
def signout(request):
    if 'email' in request.session:
        request.session.flush()
    logout(request)
    messages.success(request, "Logged out Succesfully")
    return redirect('signin')


@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'accounts/user_dashboard/dashboard.html')


def my_order(request):
    return render(request, 'accounts/user_dashboard/my_orders.html')


def my_profile(request):
    form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/user_dashboard/my_profile.html', context)


def my_address(request):
    return render(request, 'accounts/user_dashboard/my_address.html')

def my_coupon(request):
    return render(request, 'accounts/user_dashboard/my_coupon.html')

def change_password(request):
    return render(request, 'accounts/user_dashboard/change_password.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            messaage = render_to_string('accounts/password_reset_email.html',{
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                # 'phone_number' : phone_number,
                # 'uid' : user.pk,
                # 'verification_user' : verification_user,
            })
            to_mail = email
            send_male = EmailMessage(mail_subject, messaage, to=[to_mail])
            send_male.send()
            
            messages.success(request, "Password reset email has been sent to your email. Please reset your account")
            return redirect('forgotPassword')

        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgotPassword')
        
    return render(request, 'accounts/forgot_password.html')



def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')

    else:
        messages.error(request, 'This link has been expired!')
        return redirect('forgotPassword')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful ')
            return redirect('signin')

        else:
            messages.error(request, 'Password does not match!')
            return redirect('resetPassword')
    return render(request, 'accounts/reset_password.html')