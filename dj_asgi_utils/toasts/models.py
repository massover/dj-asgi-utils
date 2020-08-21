from asgiref.sync import sync_to_async
from django.conf import settings
from django.db import models


@sync_to_async
def async_create_toast(message, user_id):
    return Toast.objects.create(message=message, user_id=user_id)


class Toast(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(default="", blank=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


@sync_to_async
def async_toasts(user_id):
    return list(Toast.objects.filter(read=False, user_id=user_id).all())
