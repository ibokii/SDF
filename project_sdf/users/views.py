from django.contrib.auth import login  # type: ignore
from django.http import HttpResponseRedirect  # type: ignore
from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.views import View  # type: ignore
from .forms import CreateAccountForm, EmailAuthenticationForm, AddUserInformationForm, EditUserInfoForm  # type: ignore
from django.contrib.auth.views import LoginView  # type: ignore
from django.contrib.auth import logout  # type: ignore


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
            return HttpResponseRedirect('/add-new-user-info/')
        return render(request, self.template_name, {'form': form})


class AddUserInfoView(View):
    form_class = AddUserInformationForm
    template_name = 'registration/add_user_info.html'

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
            return HttpResponseRedirect('/home/')

        return render(request, self.template_name, {'form': form})


def user_info(request):
    user = request.user
    return render(request, 'registration/user_info.html')


def edit_profile(request):
    user = request.user
    extend_user = user.extend_profile
    if request.method == 'POST':
        form = EditUserInfoForm(request.POST, request.FILES, instance=extend_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit-user-info/')
    else:
        form = EditUserInfoForm(instance=extend_user)
    return render(request, 'registration/edit_user_info.html', {'form': form})


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('/')
