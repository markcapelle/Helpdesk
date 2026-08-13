from django.urls import path
from .views import messenger_home, fetch_messages, send_message, create_or_get, check_new, unread_status

urlpatterns = [
    path("", messenger_home, name="messenger_home"),
    path("conversation/<int:conv_id>/messages/", fetch_messages, name="fetch_messages"),
    path("send/", send_message, name="send_message"),
    path("create_or_get/<int:user_id>/", create_or_get, name="create_or_get"),
    path("conversation/<int:conv_id>/check/", check_new, name="check_new"),
    path("unread_status/", unread_status, name="unread_status"),

]
