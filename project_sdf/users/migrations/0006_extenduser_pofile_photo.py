# Generated by Django 4.1.7 on 2023-03-09 13:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_extenduser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenduser',
            name='pofile_photo',
            field=models.ImageField(default=None, upload_to='profile_photos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
        ),
    ]