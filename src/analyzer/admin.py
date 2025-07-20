from django.contrib import admin

# Register your models here.
from .models import MedicalReport, ReportFile

admin.site.register(MedicalReport)
admin.site.register(ReportFile)
