from django.contrib import admin

# import models
from news_check.models import Stock

# setup automated slug creation
class StockAdmin(admin.ModelAdmin):
    model = Stock
    list_display = ('full_name', 'symbol',)
    prepopulated_fields = {'slug': ('full_name',)}

# register it
admin.site.register(Stock, StockAdmin)