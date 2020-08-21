from django.contrib import admin

from dj_asgi_utils.toasts.models import Toast


@admin.register(Toast)
class ToastAdmin(admin.ModelAdmin):
    list_display = ["id", "message", "read", "user"]
