from django.urls import path
from . import views
urlpatterns = [
path('download_all_company_report/', views.download_all_company_report, name='download_all_company_report'),
path('download_all_farmer_report/', views.download_all_farmer_report, name='download_all_farmer_report'),
path('download_single_company_report/<int:id>', views.download_single_company_report, name='download_single_company_report'),
path('download_single_company_report_unpaid/<int:id>', views.download_single_company_report_unpaid, name='download_single_company_report_unpaid'),
path('download_single_farmer_report/<int:id>', views.download_single_farmer_report, name='download_single_farmer_report')
]