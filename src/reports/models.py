from django.db import models
import uuid

class MedicalReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    occupation = models.CharField(max_length=255, blank=True)
    symptoms = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.age})"


class ReportFile(models.Model):
    report = models.ForeignKey(MedicalReport, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='medical_reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
