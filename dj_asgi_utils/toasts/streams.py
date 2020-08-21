import asyncio

from ..core import sse
from .models import async_toasts
from .serializers import ToastSerializer


async def toast_stream(user_id):
    while True:
        toasts = await async_toasts(user_id)
        serializer = ToastSerializer(toasts, many=True)
        yield sse(serializer.data, event="toast")
        await asyncio.sleep(10)
