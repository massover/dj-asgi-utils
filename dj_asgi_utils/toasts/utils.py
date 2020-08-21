from asgiref.sync import sync_to_async


@sync_to_async
def get_user_id(request):
    return request.user.id
