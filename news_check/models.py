from django.db import models
# from news_check.api_get import *


# Create your models here.
class Stock(models.Model):
    full_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)

    def update_vibe():
        pass


class Vibe(models.Model):
    """
    happy count, sad count for title and text, updated date,
    foreign key to stock
    """
    happy_title_count = models.IntegerField(default=0)
    happy_text_count = models.IntegerField(default=0)
    sad_title_count = models.IntegerField(default=0)
    sad_text_count = models.IntegerField(default=0)
    stock = models.ForeignKey(Stock)
