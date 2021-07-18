from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('brainup_core.urls')),
    path('api/', include('brainup_core.API.urls')),
    path('auth/', include('user_manager.urls')),
    path('admin/', admin.site.urls),
]
