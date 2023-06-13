from django.contrib.auth import get_user_model  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from .forms import CreateProjectForm, EditProjectForm, TaskForm
from django.db.models import Q  # type: ignore
from django.http import HttpResponseRedirect, HttpResponse  # type: ignore
from django.shortcuts import render, get_object_or_404  # type: ignore
from django.urls import reverse_lazy  # type: ignore
from django.views import View  # type: ignore
from django.views.generic import ListView, TemplateView, CreateView  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from django.views.generic.edit import FormMixin, UpdateView, SingleObjectMixin  # type: ignore
from .models import Project, Task, Category


class HomeView(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'home.html'
	context_object_name = 'projects'

	def get_context_data(self, **kwargs):
		user = self.request.user
		context = super().get_context_data(**kwargs)
		projects = Project.objects.filter(Q(project_lead=user) | Q(project_members=user)).distinct()
		context['user_projects'] = Project.objects.filter(project_lead=user).count()
		context['projects'] = Project.objects.filter(project_members=user).count()
		context['users'] = User.objects.filter(projects__in=projects).exclude(id=user.id).distinct()
		context['tasks'] = Task.objects.filter(assigned_to=user).count()
		return context


class ProjectsListView(LoginRequiredMixin, ListView):
	model = Project
	template_name = 'projects_list.html'
	context_object_name = 'projects'

	def get_queryset(self):
		user = self.request.user
		queryset = Project.objects.all()
		# queryset = Project.objects.filter(Q(project_lead=user) | Q(project_members=user)).distinct()
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

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			project = form.save(commit=False)
			project.project_lead = self.request.user
			project.save()
			return HttpResponseRedirect(self.success_url)
		else:
			return self.form_invalid(form)


class BoarsView(LoginRequiredMixin, TemplateView):
	template_name = 'board.html'

	def get_context_data(self, **kwargs):
		project_id = self.kwargs['project_id']
		user = self.request.user
		context = super().get_context_data(**kwargs)
		project = get_object_or_404(Project, id=project_id)
		context['projects'] = project
		print(context)
		context['categories'] = Category.objects.all()
		context['tasks'] = Task.objects.filter(project=project)
		return context


def create_task(request):
	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.task_creator = request.user
			task.project = request.project
			task.save()
			return HttpResponseRedirect('')
	else:
		form = TaskForm()
	return render(request, 'create_task.html', {'form': form})


def base(request):
	return render(request, 'base.html', context={})


def profile_info(request, pk):
	project = get_object_or_404(Project, pk=pk)
	user = get_object_or_404(User, pk=project.project_lead.id)
	project_count = Project.objects.filter(project_lead=user).count()
	return render(request, 'profile_info.html', context={'project': project, 'project_count': project_count})


def edit_project(request, pk):
	instance = get_object_or_404(Project, pk=pk)
	if request.method == 'POST':
		form = EditProjectForm(request.POST, instance=instance)
		if form.is_valid():
			form.save()
			return HttpResponse(status=204, headers={'HX-Trigger': 'projectsListChanged'})
	else:
		form = EditProjectForm(instance=instance)
	context = {'form': form}
	return render(request, 'edit_project.html', context)


def delete_project(request, project_id):
	instance = get_object_or_404(Project, id=project_id)
	instance.delete()
	return HttpResponseRedirect('/my-projects/')
