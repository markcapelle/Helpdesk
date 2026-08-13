from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Conversation, Message, models



@permission_required('messenger.messenger_read', raise_exception=True)
@login_required
def messenger_home(request):
    # All users except self
    contacts = User.objects.exclude(id=request.user.id).order_by("username")

    # All conversations involving this user
    conversations = Conversation.objects.filter(
        models.Q(user1=request.user) | models.Q(user2=request.user)
    )

    return render(request, "messenger/messenger.html", {
        "contacts": contacts,
        "conversations": conversations,
    })



@permission_required('messenger.messenger_read', raise_exception=True)
@login_required
def fetch_messages(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)
    msgs = conv.messages.order_by("created_at")

    return JsonResponse({
        "messages": [
            {
                "id": m.id,
                "sender": m.sender.username,
                "body": m.body,
                "created": m.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for m in msgs
        ]
    })


@permission_required('messenger.messenger_write', raise_exception=True)
@login_required
def send_message(request):
    conv_id = request.POST.get("conversation_id")
    body = request.POST.get("body")

    conv = get_object_or_404(Conversation, id=conv_id)

    msg = Message.objects.create(
        conversation=conv,
        sender=request.user,
        body=body
    )

    return JsonResponse({"sent": True})




@permission_required('messenger.messenger_read', raise_exception=True)
@login_required
def create_or_get(request, user_id):
    other = get_object_or_404(User, id=user_id)

    conv = Conversation.objects.filter(
        models.Q(user1=request.user, user2=other) |
        models.Q(user1=other, user2=request.user)
    ).first()

    if not conv:
        conv = Conversation.objects.create(user1=request.user, user2=other)

    return JsonResponse({"conversation_id": conv.id})



@permission_required('messenger.messenger_read', raise_exception=True)
@login_required
def check_new(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)
    last_id = int(request.GET.get("last_id", 0))

    newest = conv.messages.order_by("-id").first()
    if newest and newest.id > last_id:
        return JsonResponse({"new": True})
    return JsonResponse({"new": False})