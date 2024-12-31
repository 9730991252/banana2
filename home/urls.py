from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('owner_logout/', views.owner_logout, name='owner_logout'),
    path('office_logout/', views.office_logout, name='office_logout'),
]