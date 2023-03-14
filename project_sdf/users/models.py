from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, URLValidator  # type: ignore
from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore


class ExtendUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extend_profile')
	company = models.CharField(max_length=100, default='Unknown', blank=True, null=True)
	job_title = models.CharField(max_length=100, default='Unknown', blank=True, null=True)
	first_name = models.CharField(max_length=100, default='Unknown')
	last_name = models.CharField(max_length=100, default='Unknown')
	profile_photo = models.ImageField(default='profile_photos/default_profile_photo.jpg', blank=True, null=True,
									  upload_to='profile_photos/',
									  validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
	country = models.CharField(max_length=50, default='Unknown', blank=True, null=True)
	city = models.CharField(max_length=50, default='Unknown', blank=True, null=True)
	phone_number = models.CharField(max_length=20, default='Unknown', blank=True, null=True)
	linkedin_profile = models.CharField(max_length=100, default='Unknown', blank=True, null=True)
	git_hub_profile = models.CharField(max_length=100, default='Unknown', blank=True, null=True,
									   validators=[URLValidator(schemes=['http', 'https'])])

	objects = models.Manager()

	USERNAME_FIELD = 'username'

	class Meta:
		verbose_name = "Extend User"
		verbose_name_plural = "Extend Users"

	def clean(self):
		super().clean()
		if self.git_hub_profile:
			validate_url = URLValidator(schemes=['http', 'https'])
			try:
				validate_url(self.git_hub_profile)
			except ValidationError:
				raise ValidationError("Please enter a valid GitHub profile URL")

	def __str__(self):
		return self.user.__str__()
