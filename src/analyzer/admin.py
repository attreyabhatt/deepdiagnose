from django.contrib import admin

# Register your models here.
from .models import MedicalCase, ReportFile

admin.site.register(MedicalCase)
admin.site.register(ReportFile)
