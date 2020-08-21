from dj_asgi_utils.toasts.models import Toast


def test_toast_view(client, django_user_model):
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password, read=False)
    toast = Toast.objects.create(user=user, message="hello world!")
    response = client.post(f"/api/v1/toast/{toast.id}/read/")
    assert response.status_code == 200
    toast.refresh_from_db()
    assert toast.read
