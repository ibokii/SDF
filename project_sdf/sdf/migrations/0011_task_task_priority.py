# Generated by Django 4.1.7 on 2023-03-14 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdf', '0010_alter_project_project_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('URGENT', 'URGENT')], default=None, max_length=50, null=True, verbose_name='Type'),
        ),
    ]
