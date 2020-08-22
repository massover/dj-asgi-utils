# ASGI Utils for django

A hodge-podge of asgi things for Django. None of this has been run in production.

Install it

```bash
pip install git+https://github.com/massover/dj-asgi-utils.git
```

Features and functionality

- asgi compatible runserver command with daphne
- sse
- toasts


## ASGI Runserver (using daphne)

Add it to the top of your INSTALLED_APPS in your settings

```python
INSTALLED_APPS = [
    'dj_asgi_utils.core',
]
```

Run it

```bash
./manage.py runserver --asgi
```

If you're a django dev, you might expect `./manage.py runserver` to include the ability to run an asgi devserver. `runserver` by 
default uses the stdlib WSGIServer. Currently there is no equivalent ASGI Server in the stdlib. At a high level, I had no issues 
running `uvicorn myproject.asgi:application` for local development, but then I realized that I wasn’t getting hot reloading. 
That’s easy enough to fix, and then I realized my migrations were out of date, also easy. Then I noticed I wasn’t seeing system checks or getting static files. 
These are all small things but they normally just work and they don’t for ASGI.

## SSE

1. Create a view to connect to your SSE stream
2. Create a view to serve your SSE event stream using `dj_asgi_utils.responses.AysncStreamingHttpResponse`
3. Create urls for your views
4. Use the `dj_asgi_utils.handlers.ASGIHandler`

```python

# app/views.py

import asyncio
import random
from django.http import HttpResponse
from django.urls import reverse
from dj_asgi_utils.core import sse
from dj_asgi_utils.core.responses import AysncStreamingHttpResponse

async def hello_stream(user_id):
    while True:
        option = random.choice(['world', 'moon', 'mars', 'saturn', 'universe'])
        data = {"hello": option}
        yield sse(data, event="hello")
        await asyncio.sleep(10)

async def sse_stream(request):
    stream = hello_stream(1)
    response = AysncStreamingHttpResponse(
        streaming_content=stream, content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    return response

async def view(request):
    sse_url = reverse('sse-stream')
    return HttpResponse("""
        <h1>Hello <span id="hello"></span></h1>
        <script type="text/javascript">
        const evtSource = new EventSource(%(sse_url)s);
        const element = document.getElementById("hello")
        evtSource.addEventListener("hello", function(event) {
            element.innerText = JSON.parse(event.data).hello
        });
    </script>
    """ % {"sse_url": sse_url})

# config/urls.py

from django.urls import path
from app.views import view, sse_stream

urlpatterns = [
    path("", view),
    path('sse/', sse_stream, name="sse-stream")
]

# config/asgi.py

import os
import django

from dj_asgi_utils.core.handlers import ASGIHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

def get_asgi_application():
    django.setup(set_prefix=False)
    return ASGIHandler()

application = get_asgi_application()
```

## Toasts

WIP
