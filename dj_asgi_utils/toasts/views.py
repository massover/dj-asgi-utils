from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from dj_asgi_utils.toasts.serializers import ToastSerializer

from ..core.responses import AysncStreamingHttpResponse
from .models import Toast
from .permissions import IsOwnerOrReadOnly
from .streams import toast_stream


class ToastViewSet(GenericViewSet):
    queryset = Toast.objects.all()
    serializer_class = ToastSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    @action(detail=True, methods=["post"])
    def read(self, request, pk):
        toast = self.get_object()
        toast.read = True
        toast.save()
        serializer = self.get_serializer(toast)
        return Response(serializer.data)


async def toast_stream_view(request):
    stream = toast_stream(1)
    response = AysncStreamingHttpResponse(
        streaming_content=stream, content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    return response
