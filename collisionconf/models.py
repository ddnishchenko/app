from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Person(models.Model):
    object_id = models.CharField(
        _('ID'),
        primary_key=True,
        max_length=256,
    )
    person_id = models.CharField(
        _('Person ID'),
        unique=True,
        max_length=256,
    )
    # chat_user_identity
    
    first_name = models.CharField(
        _('First Name'),
        max_length=256,
        blank=True,
        null=True
    )
    
    last_name = models.CharField(
        _('Last Name'),
        max_length=256,
        blank=True,
        null=True
    )
    
    country = models.CharField(
        _('Country'),
        max_length=256,
        blank=True,
        null=True
    )
    
    city = models.CharField(
        _('City'),
        max_length=256,
        blank=True,
        null=True
    )
    
    job_title = models.CharField(
        _('Job Title'),
        max_length=256,
        blank=True,
        null=True
    )
    
    industry = models.CharField(
        _('Industry'),
        max_length=256,
        blank=True,
        null=True
    )
    
    company_name = models.CharField(
        _('Industry'),
        max_length=256,
        blank=True,
        null=True
    )
    
    pronoun = models.CharField(
        _('Pronoun'),
        max_length=100,
        blank=True,
        null=True
    )
    
    role = models.CharField(
        _('Role'),
        max_length=128,
        blank=True,
        null=True
    )
    
    topics = models.JSONField(
        _('Topics'),
        blank=True,
        null=True
    )
    
    bio = models.TextField(
        _('Bio'),
        max_length=4096,
        blank=True,
        null=True
    )