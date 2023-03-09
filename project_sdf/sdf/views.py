from django.contrib.auth import get_user_model  # type: ignore
from django.contrib.auth.models import User

from .forms import CreateProjectForm, EditProjectForm
from django.db.models import Q  # type: ignore
from django.http import HttpResponseRedirect  # type: ignore
from django.shortcuts import render, get_object_or_404  # type: ignore
from django.urls import reverse_lazy  # type: ignore
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from django.views.generic.edit import FormMixin, UpdateView, SingleObjectMixin  # type: ignore
from .models import Project, Task, Category


class HomeView(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'home.html'
	context_object_name = 'projects'

	def get_queryset(self):
		user = self.request.user
		queryset = Project.objects.filter(Q(project_lead=user) | Q(project_members=user))
		print(queryset)
		return queryset


class MyProjectsView(LoginRequiredMixin, FormMixin, ListView):
	model = Project
	form_class = CreateProjectForm
	template_name = 'projects.html'
	context_object_name = 'projects'
	success_url = '/my-projects/'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['users'] = User.objects.all()
		return context

	def get_queryset(self):
		user = self.request.user
		queryset = Project.objects.filter(Q(project_lead=user) | Q(project_members=user)).distinct()
		return queryset

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			project = form.save(commit=False)
			project.project_lead = self.request.user
			project.save()
			return HttpResponseRedirect(self.success_url)
		else:
			return self.form_invalid(form)


class EditProjectView(LoginRequiredMixin, UpdateView):
	model = Project
	form_class = EditProjectForm
	template_name = 'edit_project.html'
	success_url = '/my-projects/'

	def get_object(self, queryset=None):
		project_id = self.kwargs.get('project_id')
		return get_object_or_404(Project, id=project_id)

	def form_valid(self, form):
		response = super().form_valid(form)
		print(form)
		return response


def delete_project(request, project_id):
	instance = get_object_or_404(Project, id=project_id)
	instance.delete()
	return HttpResponseRedirect('/my-projects/')


class BoarsView(LoginRequiredMixin, TemplateView):
	template_name = 'board.html'

	def get_context_data(self, **kwargs):
		project_id = self.kwargs['project_id']
		user = self.request.user
		context = super().get_context_data(**kwargs)
		project = get_object_or_404(Project, id=project_id)
		context['projects'] = [project]
		context['categories'] = Category.objects.all()
		context['tasks'] = Task.objects.filter(project=project)
		return context


def base(request):
	return render(request, 'base.html', context={})
