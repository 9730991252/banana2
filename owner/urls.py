from django.urls import path
from . import views
urlpatterns = [
    path('owner_home/', views.owner_home, name='owner_home'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('profile/', views.profile, name='profile'),
    path('services/', views.services, name='services'),
    path('farmer_services/', views.farmer_services, name='farmer_services'),
    path('company_services/', views.company_services, name='company_services'),

]