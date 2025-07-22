from django.urls import path
from . import views

urlpatterns = [
    path('', views.diagnose_home, name='diagnose_home'),
    path('delete-report/', views.delete_report, name='delete_report'),
    path('upload-reports/', views.upload_reports, name='upload_reports'),
]
