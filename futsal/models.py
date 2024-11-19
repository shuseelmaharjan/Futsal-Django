from django.db import models
from django.utils.text import slugify
from django.conf import settings

from users.models import CustomUser


class Futsal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    location = models.CharField(max_length=255, blank=True, null=True)  # Location name/address
    phone = models.CharField(max_length=20, blank=True, null=True)  # Phone number
    longitude = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)  # Longitude
    latitude = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)  # Latitude

    # ForeignKey to CustomUsers model (Assuming your CustomUsers model is in the same project)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
