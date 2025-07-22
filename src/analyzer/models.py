from django.db import models
import uuid
from django.contrib.auth.models import User

class MedicalCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')

    full_name = models.CharField(max_length=255, blank=True,null=True)
    age = models.PositiveIntegerField(blank=True,null=True)
    occupation = models.CharField(max_length=255, blank=True,null=True)

    symptoms = models.TextField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    diagnosis = models.TextField(blank=True,null=True)

    status = models.CharField(
        max_length=20,
        choices=[('open', 'Open'), ('closed', 'Closed'), ('under_review', 'Under Review')],
        default='open'
    )

    aggregated_text = models.TextField(blank=True,null=True)  # optional — combined OCR content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.age}) - {self.status}"


def user_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"medical_reports/{instance.user.id}/{filename}"

class ReportFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    case = models.ForeignKey('MedicalCase', on_delete=models.CASCADE, null=True, blank=True, related_name='files')

    file = models.FileField(upload_to=user_upload_path)
    original_name = models.CharField(max_length=255)
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name


