from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login


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
