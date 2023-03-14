from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django import forms  # type: ignore
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.urls import reverse

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

    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username.'}),
        'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email.'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = self.widgets.get(field_name)
            if widget:
                field.widget.attrs.update(widget.attrs)


class AddUserInformationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    company = forms.CharField(max_length=100)
    job_title = forms.CharField(max_length=100)

    class Meta:
        model = ExtendUser
        fields = ('first_name', 'last_name', 'company', 'job_title')

    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name.'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name.'}),
        'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your company name.'}),
        'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your company name.'}),

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = self.widgets.get(field_name)
            if widget:
                field.widget.attrs.update(widget.attrs)


class EditUserInfoForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = reverse("delete_project", args=[self.instance.id])
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save')),
        self.helper.add_input(Button(
            'delete',
            'Delete',
            onclick=f'window.location.href="{self.url}"')
        )

    class Meta:
        model = ExtendUser
        fields = ['profile_photo', 'first_name', 'last_name']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditUserInfoForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = reverse("delete_project", args=[self.instance.id])
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save')),
        self.helper.add_input(Button(
            'delete',
            'Delete',
            onclick=f'window.location.href="{self.url}"')
        )

    class Meta:
        model = ExtendUser
        fields = ['company', 'job_title', 'country', 'city', 'phone_number', 'linkedin_profile', 'git_hub_profile']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_profile': forms.TextInput(attrs={'class': 'form-control'}),
            'git_hub_profile': forms.TextInput(attrs={'class': 'form-control'}),
        }
