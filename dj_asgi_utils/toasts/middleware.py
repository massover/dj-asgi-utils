import asyncio

from django.template.backends.utils import csrf_input
from django.templatetags import static
from django.utils.decorators import sync_and_async_middleware

_HTML_TYPES = ("text/html", "application/xhtml+xml")


@sync_and_async_middleware
def toast_middleware(get_response):
    # One-time configuration and initialization goes here.
    if asyncio.iscoroutinefunction(get_response):

        async def middleware(request):
            # Do something here!
            response = await get_response(request)
            response = toast_response(request, response)
            return response

    else:

        def middleware(request):
            # Do something here!
            response = get_response(request)
            response = toast_response(request, response)
            return response

    return middleware


# middleware are usually classes
ToastMiddleware = toast_middleware


def toast_response(request, response):
    content_encoding = response.get("Content-Encoding", "")
    content_type = response.get("Content-Type", "").split(";")[0]
    if any(
        (
            getattr(response, "streaming", False),
            "gzip" in content_encoding,
            content_type not in _HTML_TYPES,
            request.is_ajax(),
        )
    ):
        return response
    content = response.content.decode(response.charset)
    notyf_css = static.static("toasts/css/notyf.min.css")
    head = """
    <link rel=\"stylesheet\" href=\"%(notyf_css)s\">
    </head>
    """ % {
        "notyf_css": notyf_css
    }
    content = content.replace("</head>", head)
    js = static.static("toasts/js/dj-asgi-utils.toast.js")
    notyf_js = static.static("toasts/js/notyf.min.js")
    body = """
    <script src=\"%(notyf_js)s\"></script>
    %(csrf_input)s
    <script src=\"%(js)s\"></script>
    </body>
    """ % {
        "notyf_js": notyf_js,
        "js": js,
        "csrf_input": csrf_input(request),
    }
    content = content.replace("</body>", body)
    response.content = content
    if "Content-Length" in response:
        response["Content-Length"] = len(response.content)
    return response
