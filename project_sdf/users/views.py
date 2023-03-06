from django.contrib.auth import login  # type: ignore
from django.http import HttpResponseRedirect  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from django.views import View  # type: ignore
from .forms import CreateAccountForm, EmailAuthenticationForm, AddUserInformationForm  # type: ignore
from django.contrib.auth.views import LoginView  # type: ignore
from django.contrib.auth import logout  # type: ignore


class MyLoginView(LoginView):
    template_name = "new_login"
    authentication_form = EmailAuthenticationForm


class CreateAccountView(View):
    form_class = CreateAccountForm
    template_name = 'registration/new_create_account.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='users.backends.EmailBackend')
            return HttpResponseRedirect('/add-new-user-info/')
        return render(request, self.template_name, {'form': form})


class AddUserInfoView(View):
    form_class = AddUserInformationForm
    template_name = 'registration/new_add_user_info.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)

        if form.is_valid():
            extend_user = form.save(commit=False)
            extend_user.user_id = request.user.id
            extend_user.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('/')
