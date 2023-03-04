from django.db.models import Q  # type: ignore
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404  # type: ignore
from django.urls import reverse_lazy  # type: ignore
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from .models import Project, Task, Category  # type: ignore
from .forms import ProjectForm  # type: ignore


class HomeView(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'home.html'
	context_object_name = 'projects'

	def get_queryset(self):
		user = self.request.user
		return Project.objects.filter(
			Q(project_lead=user) | Q(project_members=user)
		)


class MyProjectsView(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'projects.html'
	context_object_name = 'projects'

	def get_queryset(self):
		user = self.request.user
		return Project.objects.filter(
			Q(project_lead=user) | Q(project_members=user)
		)


class CreateProjectView(LoginRequiredMixin, View):
	form_class = ProjectForm
	template_name = 'create_project.html'
	success_url = '/my-projects/'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			project = form.save(commit=False)
			project.project_lead = request.user
			project.save()
			return HttpResponseRedirect(self.success_url)
		return render(request, self.template_name, {'form': form})


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

def board(request):
	return render(request, 'board.html', context={})
