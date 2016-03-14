from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# from news_check.api_get import *


# Create your models here.
class Company(models.Model):
    full_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    industry = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    lat = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    lon = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    state = models.CharField(max_length=3, null=True)
    city = models.CharField(max_length=50, null=True)

    def update_vibe():
        pass

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(self.full_name)
        super(Company, self).save(*args, **kwargs)


class Vibe(models.Model):
    """
    happy count, sad count for title and text, updated date,
    foreign key to stock
    """
    happy_title_count = models.IntegerField(default=0)
    happy_text_count = models.IntegerField(default=0)
    sad_title_count = models.IntegerField(default=0)
    sad_text_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(Company)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Vibe, self).save(*args, **kwargs)
