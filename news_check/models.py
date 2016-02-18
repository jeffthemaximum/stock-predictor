from django.db import models

# Create your models here.
class Stock(models.Model):
    full_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)