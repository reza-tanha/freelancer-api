from django.contrib import admin
from django.urls import path, include
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls', namespace='api')),
]
if settings.DEBUG:
    urlpatterns +=[
        path("__debug__/", include("debug_toolbar.urls")),
    ]

