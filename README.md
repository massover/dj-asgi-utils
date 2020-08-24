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

Real time toast notifications using SSE

Uses:

- [notyfjs](https://github.com/caroso1222/notyf) to not reinvent toast messages.
- [djangorestframework](https://www.django-rest-framework.org/) because it's more fun to code an api with drf than without it.

### Quickstart

Add the toasts application to your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    'dj_asgi_utils.toasts',
]
```

Add `dj_asgi_utils.toasts.middleware.ToastMiddleware` to your `MIDDLEWARE`

```python
MIDDLEWARE = [
    ...,
    "dj_asgi_utils.toasts.middleware.ToastMiddleware",
]
```

Run your migrations

```bash
./manage.py migrate
```

Open your browser to your admin, eg

```
open http://localhost:8000/admin/
```

While the admin is open in the browser, load the shell, and create a toast. You should see the toast flash in the admin!

```python
from django.contrib.auth import get_user_model
from dj_asgi_utils.toasts.models import create_toast

User = get_user_model()
user_id = User.objects.get().id
# Note, we create in the shell with the sync `create_toast` function
# You may use be using `async_create_toast` in an async view.
create_toast("Hello world!", user_id)
```

### Toasts without middleware

If you need finer control on which views see the toast, you can update your templates to include the js and css.

The following extends the default `base_site.html` to work with toasts without using the middleware.

```html
{% extends 'admin/base_site.html' %}

{% block extrastyle %}
    {{ block.super }}
    <link rel="stylesheet" href="{% static "toasts/css/notyf.min.css" %}">
{% endblock %}

{% block extrahead %}
    {{ block.super }}
    <script src="{% static "toasts/js/notyf.min.js" %}></static>

{% endblock %}

{% block footer %}
    {% csrf_token %}
    <script src="{% static "toasts/js/dj-asgi-utils.toast.js" %}></static>
{% endblock %}
```
