from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms  # type: ignore
from .models import Project, Task


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


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = '__all__'
		widgets = {
			'task_summary': forms.TextInput(attrs={'class': 'form-control'}),
			'task_status': forms.Select(attrs={'class': 'form-control'}),
			'task_type': forms.Select(attrs={'class': 'form-control'}),
			'task_priority': forms.Select(attrs={'class': 'form-control'}),
			'task_category': forms.Select(attrs={'class': 'form-control'}),
			'project': forms.Select(attrs={'class': 'form-control'}),
			'task_url': forms.URLInput(attrs={'class': 'form-control'}),
			'task_description': forms.Textarea(attrs={'class': 'form-control'}),
			'files': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
			'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'assigned_to': forms.Select(attrs={'class': 'form-control'}),
		}
