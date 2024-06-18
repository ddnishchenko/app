from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import admin, messages
from django.core.management import call_command
from django.shortcuts import redirect
from django.forms import Media
import logging

logger = logging.getLogger(__name__)

from collisionconf import models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'first_name', 'last_name', 'country', 'job_title', 'industry', 'role')
    list_display_links = ('object_id',)
    list_filter = ('country', 'job_title', 'industry', 'role')
    search_fields = ('first_name', 'last_name', 'job_title')
    search_help_text = _('Searching by title and description')
    save_on_top = True

