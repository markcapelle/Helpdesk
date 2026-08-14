from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Conversation, Message, models


#-----------------------------
# Has unread messages
#-----------------------------
def has_unread_messages(user, other):
    conv = Conversation.objects.filter(
        models.Q(user1=user, user2=other) |
        models.Q(user1=other, user2=user)
    ).first()

    if not conv:
        return False

    return conv.messages.filter(sender=other).exclude(seen_by=user).exists()






#-----------------------------
# Messenger home
#-----------------------------
@permission_required('messenger.messenger_read', raise_exception=True)
@login_required
def messenger_home(request):
    contacts = User.objects.exclude(id=request.user.id).order_by("username")

    enriched = []
    for c in contacts:
        enriched.append({
            "user": c,
            "has_unread": has_unread_messages(request.user, c)
        })

    return render(request, "messenger/messenger.html", {
        "contacts": enriched,
    })




#-----------------------------
# Fetch messages
#-----------------------------
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



#-----------------------------
# Send message
#-----------------------------
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



#-----------------------------
# Create or Get
#-----------------------------
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

    # Mark all messages from OTHER as seen
    conv.messages.filter(sender=other).exclude(seen_by=request.user).update()

    for msg in conv.messages.filter(sender=other):
        msg.seen_by.add(request.user)

    return JsonResponse({"conversation_id": conv.id})




#-----------------------------
# Check new
#-----------------------------
@permission_required('messenger.messenger_read', raise_exception=True)
@login_required
def check_new(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)
    last_id = int(request.GET.get("last_id", 0))

    newest = conv.messages.order_by("-id").first()

    if newest and newest.id > last_id:
        # Mark all messages from OTHER as read
        other_user = conv.user1 if conv.user2 == request.user else conv.user2

        unread_msgs = conv.messages.filter(sender=other_user).exclude(seen_by=request.user)

        for msg in unread_msgs:
            msg.seen_by.add(request.user)

        return JsonResponse({"new": True})

    return JsonResponse({"new": False})







#-----------------------------
# Unread status
#-----------------------------
@login_required
def unread_status(request):
    contacts = User.objects.exclude(id=request.user.id)
    result = {}

    for c in contacts:
        conv = Conversation.objects.filter(
            models.Q(user1=request.user, user2=c) |
            models.Q(user1=c, user2=request.user)
        ).first()

        if not conv:
            result[c.id] = False
            continue

        unread = conv.messages.filter(sender=c).exclude(seen_by=request.user).exists()

        result[c.id] = {
            "unread": unread,
            "conversation_id": conv.id,
            "other_user_id": c.id,
        }

    return JsonResponse(result)
