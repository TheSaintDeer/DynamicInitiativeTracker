from django.contrib import admin

from . import models


admin.site.register(models.Creature)
admin.site.register(models.Tracker)