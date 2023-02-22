from django.db import models
from django.contrib.auth.models import User


class ExtendUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	company = models.CharField(max_length=100)
	job_title = models.CharField(max_length=100)

	object = models.Manager()

	class Meta:
		verbose_name = "Extend User"
		verbose_name_plural = "Extend Users"

	def __str__(self):
		return self.user.__str__()

	def __repr__(self):
		return f'Note object: {self.user.__str__()}'
