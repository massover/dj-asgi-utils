import asyncio

from django.shortcuts import redirect
from django.shortcuts import render

from dj_asgi_utils.toasts.models import async_create_toast
from dj_asgi_utils.toasts.utils import get_user_id
from example.forms import ToastForm


async def toast_demo(request):
    form = ToastForm(request.POST or None)
    if request.method == "POST" and form.is_valid():

        async def sleep_task(user_id):
            message = f"Sleep running for at least {form.cleaned_data['sleep_time']} second(s)..."
            await async_create_toast(message, user_id)
            await asyncio.sleep(form.cleaned_data["sleep_time"])
            await async_create_toast(form.cleaned_data["message"], user_id)

        user_id = await get_user_id(request)
        loop = asyncio.get_event_loop()
        loop.create_task(sleep_task(user_id))
        return redirect("toast-demo")

    context = {"form": form}
    return render(request, "example/toast_demo.html", context=context)
