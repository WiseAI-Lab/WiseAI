from django.contrib import admin

# Register your models here.
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from .models import ConfigurationModel


@admin.register(ConfigurationModel)
class ConfigurationAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ('id', 'name', 'content')
    list_display_links = ('id', 'name', 'content')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
