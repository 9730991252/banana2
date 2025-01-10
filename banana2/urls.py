from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
urlpatterns = [
    path('', include('home.urls')),
    path('sunil/', include('sunil.urls')),
    path('ajax/', include('ajax.urls')),
    path('office/', include('office.urls')),
    path('owner/', include('owner.urls')),
    path('report/', include('report.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
