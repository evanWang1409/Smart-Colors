from django.db import models

# Create your models here.
class pic(models.Model):
    hexValue = models.CharField(max_length=7)
    url = models.CharField(max_length=200)
    