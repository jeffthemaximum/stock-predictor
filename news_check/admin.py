from django.contrib import admin

# import models
from news_check.models import Company


# setup automated slug creation
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('full_name', 'symbol',)
    prepopulated_fields = {'slug': ('full_name',)}

# register it
admin.site.register(Company, CompanyAdmin)
