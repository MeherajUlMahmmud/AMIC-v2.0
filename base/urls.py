from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_control.urls')),
    path('appointments/', include('appointment_control.urls')),
    path('articles/', include('article_control.urls')),
    path('emergency/', include('emergency_service_control.urls')),
    path('health-advisor/', include('health_advisor_control.urls')),
    path('ot/', include('ot_control.urls')),
    path('patient-community/', include('patient_community_control.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
