from django.core.validators import FileExtensionValidator
from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore


class ExtendUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extend_profile')
	company = models.CharField(max_length=100, default='1')
	job_title = models.CharField(max_length=100, default='1')
	first_name = models.CharField(max_length=100, default='1')
	last_name = models.CharField(max_length=100, default='1')
	profile_photo = models.ImageField(default='profile_photos/default_profile_photo.jpg', blank=True, null=True,
									  upload_to='profile_photos/',
									  validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

	objects = models.Manager()

	USERNAME_FIELD = 'username'

	class Meta:
		verbose_name = "Extend User"
		verbose_name_plural = "Extend Users"

	def __str__(self):
		return self.user.__str__()
