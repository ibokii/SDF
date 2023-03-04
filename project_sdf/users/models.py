from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore


class ExtendUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	company = models.CharField(max_length=100, default='1')
	job_title = models.CharField(max_length=100, default='1')
	first_name = models.CharField(max_length=100, default='1')
	last_name = models.CharField(max_length=100, default='1')

	object = models.Manager()

	USERNAME_FIELD = 'username'

	class Meta:
		verbose_name = "Extend User"
		verbose_name_plural = "Extend Users"

	def __str__(self):
		return self.user.__str__()

