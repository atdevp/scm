from django.views.generic.base import View
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, HttpResponseRedirect


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")


class LoginView(View):
    def get(self, request, *args, **kwargs):
        isLogin = request.session.get('is_login')
        if not isLogin:
            return render(request, 'login.html')
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        u = authenticate(email=email, password=password)
        if u is None:
            return render(request, 'login.html')

        isActive = u.is_active
        if not isActive:
            return render(request, 'login.html')

        login(request, u)
        request.session['is_login'] = True
        return HttpResponseRedirect('/')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        isLogin = request.session.get('is_login')
        if not isLogin:
            return render(request, 'login.html')
        return render(request, 'index.html')
