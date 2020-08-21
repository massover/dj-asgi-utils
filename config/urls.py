from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/", admin.site.urls),
    path("", include("dj_asgi_utils.toasts.urls")),
    path("", include("example.urls")),
]
