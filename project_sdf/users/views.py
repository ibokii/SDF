from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateAccountForm, EmailAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout


class MyLoginView(LoginView):
    template_name = "login"
    authentication_form = EmailAuthenticationForm


class CreateAccountView(View):
    form_class = CreateAccountForm
    template_name = 'registration/create_account.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='users.backends.EmailBackend')
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


# class AddUserInfoView(View):
#     form_class = AddUserInformationForm
#     template_name = 'registration/add_user_info.html'
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user, backend='users.backends')
#             return HttpResponseRedirect('/')
#         return render(request, self.template_name, {'form': form})


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('login')
