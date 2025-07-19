from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ReportFile
from django.utils.timezone import now

@login_required
def upload_reports(request):
    uploaded_files = []
    errors = []

    if request.method == "POST":
        files = request.FILES.getlist("files")
        for f in files:
            try:
                # Automatically saved to correct user path by model's upload_to
                report_file = ReportFile.objects.create(
                    user=request.user,
                    file=f,
                    original_name=f.name,
                    uploaded_at=now(),
                )

                # Generate signed URL (requires querystring_auth = True)
                signed_url = report_file.file.url
                uploaded_files.append({
                    "url": signed_url,
                    "name": f.name,
                })


            except Exception as e:
                errors.append(f"{f.name}: {str(e)}")

    existing_reports = ReportFile.objects.filter(user=request.user).order_by('-uploaded_at')

    return render(request, "reports/upload.html", {
        "uploaded": uploaded_files,
        "errors": errors,
        "existing_reports": existing_reports,
    })

