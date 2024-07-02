from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from .forms import UserSinupForm, ProfileForm
from .models import User, EmailConfirm
from django.core.mail import send_mail
from datetime import datetime, timedelta
from dateutil import tz


def send_email(email, code, your_request_type, email_send_type):
    subject = f"ایمیل {your_request_type}"
    base_link = 'http://127.0.0.1:8000'
    # forget_password_link = 
    link = 'forgetPassword/confirm' if email_send_type == 'forget_password' else 'sinup/active'
    target_link = f'{base_link}/{link}/{email}/{code}'
    message = f"سلام. این ایمیل به دلیل درخواست {your_request_type} برای شما ارسال شده است.\n درصورتی که این درخواست از سوی شما نبوده آن را نادیده بگیرید.\n جهت ادامه روی لینک زیر بزنید\n {target_link}"
    from_email = ''
    recipient_list = [email]
    response = send_mail(subject, message, from_email, recipient_list)
    return response



class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        context = {}
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # if request have next url
                next = request.GET.get('next', None)
                return redirect(next) if next else redirect('home')
            else:
                context.update({'msg': 'email or password error'})
        else:
            context.update({'msg': 'not valid'})
        return render(request, self.template_name, context)


class SinupView(View):
    template_name = 'auth/sinup.html'

    def get(self, request, *args, **kwargs):
        context = {
            'sinupForm': UserSinupForm(),
            'profileForm': ProfileForm(),
            }
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        sinupForm = UserSinupForm(request.POST)
        profileForm = ProfileForm(request.POST)
        context = {'sinupForm': sinupForm, 'profileForm': profileForm}

        if profileForm.is_valid():
            if sinupForm.is_valid():
                password = sinupForm.cleaned_data['password1']
                email = sinupForm.cleaned_data['email']
                user = sinupForm.save(commit=False)
                user.set_password(password)
                user.save()
                profile = profileForm.save(commit=False)
                profile.user=user
                profile.save()
                otp = EmailConfirm.objects.create(email=email, otp_type='S', expire=datetime.now() + timedelta(minutes=5))
                send_email(email, otp.code, 'فعال سازی اکانت', 'acctive_account')
                context.update({'sinupForm_msg': 'success'})
            else:
                context.update({'sinupFrom_msg': 'not valid'})
        else:
            context.update({'profileFrom_msg': 'not vlaid'})
        return render(request, self.template_name, context)


class ActiveAccountView(View):
    template_name = 'auth/active_account.html'

    def get(self, request, email, code, *args, **kwargs):
        try:
            otp = EmailConfirm.objects.get(email=email, code=code, otp_type='S', expire__gte=datetime.now(tz.UTC))
            otp.delete()
            User.objects.filter(email=email).update(is_active=True)
            return redirect('profile')
        except:
            return redirect('home')
