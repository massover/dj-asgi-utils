from django.urls import path

from example.views import asyncio_sleep_task, toast_demo

urlpatterns = [
    path("toast/demo/", toast_demo, name="toast-demo"),
    path("asyncio-sleep-task/", asyncio_sleep_task, name="asyncio-sleep-task"),
]
