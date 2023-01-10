import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("Users", self.username, instance)
        return None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField("Description", max_length=600, default='', blank=True)
    image = models.ImageField( upload_to=image_upload_to)

    def __str__(self):
        return self.username
