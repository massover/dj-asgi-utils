from django.urls import include, path
from rest_framework import routers

from .views import ToastViewSet, toast_stream_view

router = routers.SimpleRouter()
router.register(r"toast", ToastViewSet)

urlpatterns = [
    path("api/v1/", include((router.urls, "toasts"), namespace="toasts")),
    path("api/v1/toast/stream/", toast_stream_view, name="toast-stream"),
]
