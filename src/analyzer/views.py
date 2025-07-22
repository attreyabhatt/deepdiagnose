from django.shortcuts import render
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import ReportFile,MedicalCase
from django.db.models import Prefetch
from django.template.loader import render_to_string

def diagnose_home(request):
    medical_cases = MedicalCase.objects.filter(user=request.user).prefetch_related(
        Prefetch('files', queryset=ReportFile.objects.all())
    )
    if medical_cases.exists():
        pass
    else:
        medical_cases = MedicalCase.objects.create(
                        user=request.user,
        )
    
    return render(request, "analyzer/main.html", {
        'medical_cases': medical_cases,
    })

allowed_content_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']

def upload_reports(request):
    
    if request.method == "POST" and request.user.is_authenticated:
        files = request.FILES.getlist('files')
        created_reports = []
        errors = []

        for file in files:
            if file.content_type not in allowed_content_types:
                errors.append(f"{file.name}: Unsupported file type")
                continue
            try:
                report = ReportFile.objects.create(
                    user=request.user,
                    file=file,
                    original_name=file.name
                )
                created_reports.append(report)
            except Exception as e:
                errors.append(f"{file.name}: {str(e)}")

        if created_reports:
            html = ""
            for report in created_reports:
                html += render_to_string("partials/report_card.html", {"report": report})
            return JsonResponse({"success": True, "new_reports_html": html})
        return JsonResponse({"success": False, "errors": errors})
    
    return JsonResponse({"success": False, "errors": ["Unauthorized or invalid request"]})

@require_POST
@login_required
@csrf_protect
def delete_report(request):
    report_id = request.POST.get("report_id")
    try:
        report = ReportFile.objects.get(id=report_id, user=request.user)
        if report.file:
            report.file.delete(save=False)
        report.delete()
        return JsonResponse({"success": True})
    except ReportFile.DoesNotExist:
        return JsonResponse({"success": False, "error": "Report not found."}, status=404)
