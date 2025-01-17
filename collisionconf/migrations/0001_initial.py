# Generated by Django 4.1 on 2024-06-14 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('object_id', models.CharField(max_length=256, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=256, unique=True, verbose_name='Person ID')),
                ('first_name', models.CharField(blank=True, max_length=256, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=256, verbose_name='Last Name')),
                ('country', models.CharField(blank=True, max_length=256, verbose_name='Country')),
                ('city', models.CharField(blank=True, max_length=256, verbose_name='City')),
                ('job_title', models.CharField(blank=True, max_length=256, verbose_name='Job Title')),
                ('industry', models.CharField(blank=True, max_length=256, verbose_name='Industry')),
                ('company_name', models.CharField(blank=True, max_length=256, verbose_name='Industry')),
                ('pronoun', models.CharField(blank=True, max_length=100, verbose_name='Pronoun')),
                ('role', models.CharField(blank=True, max_length=128, verbose_name='Role')),
                ('topics', models.JSONField(blank=True, verbose_name='Topcs')),
                ('bio', models.TextField(blank=True, max_length=4096, verbose_name='Bio')),
            ],
        ),
    ]
