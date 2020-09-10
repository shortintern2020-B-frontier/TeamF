from django.db import models
from django.contrib.auth.models import User


class ImageChoice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url_path = models.CharField(max_length=100)

    def __str__(self):
        return self.url_path

    def __iter__(self):
        return self.url_path.__iter__()
