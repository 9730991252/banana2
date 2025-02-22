from django.urls import path
from . import views

urlpatterns = [
    path('', views.sunil_login, name='sunil_login'),
    path('sunil_home/', views.sunil_home, name='sunil_home'),
    path('payment_detail/', views.payment_detail, name='payment_detail'),
    path('shope_detail/<int:id>', views.shope_detail, name='shope_detail'),
]