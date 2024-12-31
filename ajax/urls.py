from django.urls import path
from . import views
urlpatterns = [
    path('farmer_check/', views.farmer_check, name='farmer_check'),
    path('search_farmer_bill/', views.search_farmer_bill, name='search_farmer_bill'),
    path('select_bill/', views.select_bill, name='select_bill'),
    path('save_company/', views.save_company, name='save_company'),
    path('check_company/', views.check_company, name='check_company'),
]