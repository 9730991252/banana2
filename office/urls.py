from django.urls import path
from . import views
urlpatterns = [
    path('office_home/', views.office_home , name='office_home'),
    path('new_farmer_bill/', views.new_farmer_bill, name='new_farmer_bill'),
    path('farmer_bill/', views.farmer_bill, name='farmer_bill'),
    path('farmer/', views.farmer, name='farmer'),
    path('view_farmer_bill/<int:id>', views.view_farmer_bill, name='view_farmer_bill'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('profile/', views.profile, name='profile'),
    path('signature/', views.signature, name='signature'),
    path('company/', views.company, name='company'),
    path('new_company_bill/', views.new_company_bill, name='new_company_bill'),
    path('view_company_bill/<int:id>', views.view_company_bill, name='view_company_bill'),
    path('company_bill/', views.company_bill, name='company_bill'),
    path('logo/', views.logo, name='logo'),
]