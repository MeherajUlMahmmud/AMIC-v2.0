from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_control.urls')),
    path('appointments/', include('appointment_control.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
