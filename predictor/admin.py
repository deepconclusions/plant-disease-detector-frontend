from django.contrib import admin
from .models import Image, Secret

# Register your models here.
admin.site.register(model_or_iterable=[Image, Secret])
