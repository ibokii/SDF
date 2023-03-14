from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms  # type: ignore
from .models import Project


class CreateProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = [
			'project_title',
			'project_url',
			'project_type',
			'project_description',
		]
		widgets = {
			'project_title': forms.TextInput(attrs={'class': 'form-control',
													'autofocus': True, 'placeholder': 'Enter project name'}),
			'project_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter project URL'}),
			'project_type': forms.Select(attrs={'class': 'form-control'}),
			'project_description': forms.Textarea(attrs={'class': 'form-control'}),
		}


class EditProjectForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.add_input(Submit('submit', 'Save')),

	class Meta:
		model = Project
		fields = [
			'project_title',
			'project_url',
			'project_type',
			'project_description',
			'project_members',
		]
		widgets = {
			'project_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
			'project_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter project URL'}),
			'project_type': forms.Select(attrs={'class': 'form-control'}),
			'project_description': forms.Textarea(attrs={'class': 'form-control'}),
			'project_members': forms.SelectMultiple(attrs={'class': 'form-control'}),
		}
