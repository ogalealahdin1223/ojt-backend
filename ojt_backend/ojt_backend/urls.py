from django.contrib import admin
from django.urls import path, include
from api.views import login_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # login
    path('api/login/', login_view),

    # attendance routes
    path('api/', include('attendance.urls')),

    # users/admin routes
    path('api/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)