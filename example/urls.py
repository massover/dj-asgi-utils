from django.urls import path

from example.views import toast_demo

urlpatterns = [
    path("toast/demo/", toast_demo, name="toast-demo"),
]
