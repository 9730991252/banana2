from django.urls import path
from . import views
urlpatterns = [
    path('farmer_check/', views.farmer_check, name='farmer_check'),
    path('select_bill/', views.select_bill, name='select_bill'),
    path('save_company/', views.save_company, name='save_company'),
    path('check_company/', views.check_company, name='check_company'),
    path('select_company/', views.select_company, name='select_company'),
    path('search_company/', views.search_company, name='search_company'),
]