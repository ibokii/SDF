from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import ExtendUser


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'autofocus': True}),
        label="Email",
        required=True,
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct email address and password. "
            "Note that both fields may be case-sensitive."
        ),
        'inactive': "This account is inactive.",
    }


class CreateAccountForm(UserCreationForm):
    username = forms.CharField(max_length=30, min_length=2)
    email = forms.EmailField(max_length=90, widget=forms.TextInput(attrs={'autofocus': True}))
    password1 = forms.CharField(min_length=4, max_length=18, widget=forms.PasswordInput, label='Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different email address.')
        return email


class AddUserInformationForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.')
    company = forms.CharField(max_length=100, help_text='Enter your company name.')
    job_title = forms.CharField(max_length=100, help_text='Enter your company name.')

    class Meta:
        model = ExtendUser
        fields = ('first_name', 'last_name', 'company', 'job_title')
