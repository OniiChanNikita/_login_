from django.db import models

# Create your models here.
from django.urls import reverse


class EmailIndentefication(models.Model):
    username = models.CharField(max_length=255, unique = True)
    status_account = models.CharField(default="no", max_length=5)
    slug_indentefication = models.SlugField(max_length = 20, unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('url_activate', kwargs = {'abs_slug_indentefication': self.slug_indentefication})