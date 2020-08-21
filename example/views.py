import asyncio

from django.contrib import messages
from django.shortcuts import redirect, render

from dj_asgi_utils.toasts.models import async_create_toast
from dj_asgi_utils.toasts.utils import get_user_id
from example.forms import ToastForm


async def asyncio_sleep_task(request):
    async def sleep_task(user_id):
        await asyncio.sleep(10)
        await async_create_toast("hello world!", user_id)

    user_id = await get_user_id(request)
    loop = asyncio.get_event_loop()
    loop.create_task(sleep_task(user_id))
    messages.success(request, "Waiting for toast")
    return redirect("toast-demo")


async def toast_demo(request):
    form = ToastForm()
    context = {"form": form}
    return render(request, "example/toast_demo.html", context=context)
