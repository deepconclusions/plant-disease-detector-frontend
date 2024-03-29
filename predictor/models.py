from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    name = models.CharField(max_length=255, default="image")
    image = models.FileField(upload_to='images/')
    user = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.name


class Secret(models.Model):
    name = models.CharField(max_length=255, default="secret")
    value = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name
