from django.urls import path
from . import views
urlpatterns = [
    path('farmer_check/', views.farmer_check, name='farmer_check'),
    path('select_bill/', views.select_bill, name='select_bill'),
    path('save_company/', views.save_company, name='save_company'),
    path('check_company/', views.check_company, name='check_company'),
    path('select_company/', views.select_company, name='select_company'),
    path('search_company/', views.search_company, name='search_company'),
    path('save_date_company_bill/', views.save_date_company_bill, name='save_date_company_bill'),
    path('save_date_farmer_bill/', views.save_date_farmer_bill, name='save_date_farmer_bill'),
    path('add_leaf_weight_farmer_services/', views.add_leaf_weight_farmer_services, name='add_leaf_weight_farmer_services'),
    path('chang_farmer_bill_paid_status/', views.chang_farmer_bill_paid_status, name='chang_farmer_bill_paid_status'),
    path('add_danda_weight_company_services/', views.add_danda_weight_company_services, name='add_danda_weight_company_services'),
]