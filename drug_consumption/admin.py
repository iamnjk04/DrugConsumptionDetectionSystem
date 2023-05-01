from django.contrib import admin
from .models import Patient, Admin, DatasetTable, Result
# Register your models here.
admin.site.register(Patient)
admin.site.register(Admin)
admin.site.register(DatasetTable)
admin.site.register(Result)