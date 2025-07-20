from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_reports, name='upload_reports'),
]
