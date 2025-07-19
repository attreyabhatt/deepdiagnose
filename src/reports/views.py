from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

def upload_reports(request):
    uploaded_files = []
    errors = []

    if request.method == "POST":
        files = request.FILES.getlist("files")
        for f in files:
            try:
                saved_path = default_storage.save(f"{f.name}", ContentFile(f.read()))
                uploaded_files.append(saved_path)
            except Exception as e:
                errors.append(f"{f.name}: {str(e)}")

    return render(request, "reports/upload.html", {
        "uploaded": uploaded_files,
        "errors": errors,
    })
