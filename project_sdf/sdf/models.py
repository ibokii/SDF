from django.contrib.auth.models import User  # type: ignore
from django.db import models  # type: ignore


class Project(models.Model):
	PROJECT_TYPES = (  # Fix
		('Scrum', 'Scrum software development'),
		('Kanban', 'Kanban software development'),
		('Basic', 'Basic software development'),
	)

	project_title = models.CharField(max_length=255, verbose_name='Title')
	project_url = models.URLField(verbose_name='URL', blank=True)
	project_type = models.CharField(max_length=10, choices=PROJECT_TYPES, verbose_name='Type')
	project_description = models.TextField(verbose_name='Description', blank=True)
	project_lead = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leading_projects',
									 verbose_name='Lead')
	project_members = models.ManyToManyField(User, related_name='projects', blank=True, verbose_name='Member')
	create_date = models.DateField(auto_now_add=True, verbose_name='Create date')
	update_date = models.DateField(auto_now=True, verbose_name='Update date')

	objects = models.Manager()

	class Meta:
		verbose_name = 'Project'
		verbose_name_plural = 'Projects'

	def __str__(self):
		return self.project_title

	def __repr__(self):
		return f'Project model: {self.project_title}'


class Category(models.Model):
	category_title = models.CharField(max_length=255, verbose_name='Tittle')

	objects = models.Manager()

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.category_title

	def __repr__(self):
		return f'Category model: {self.category_title}'


class Task(models.Model):
	task_summary = models.CharField(max_length=100, verbose_name='Summary')
	task_status = models.CharField(max_length=20, choices=(
		('To do', 'To do'),
		('In progress', 'In Progress'),
		('Done', 'Done'),
	), default='New')
	task_type = models.CharField(max_length=50, verbose_name='Type', null=True, choices=(
		('Task', 'Task'),
		('Story', 'Story'),
		('Bug', 'Bug'),
		('Feature', 'Feature')
	), default=None)
	task_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Category')
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
	task_url = models.URLField(verbose_name='URL', blank=True)
	task_description = models.TextField(verbose_name='Description')
	files = models.ManyToManyField('File', blank=True, related_name='tasks', verbose_name='Files')  # Fix
	create_date = models.DateField(auto_now_add=True, verbose_name='Create date')
	update_date = models.DateField(auto_now=True, verbose_name='Update date')
	due_date = models.DateField(verbose_name='Due date', null=True, blank=True)
	task_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leading_task',
									 verbose_name='Creator')
	assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

	objects = models.Manager()

	def __str__(self):
		return self.task_summary


class File(models.Model):
	file = models.FileField(blank=False, null=False)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	objects = models.Manager()

	def __str__(self):
		return self.file.name
