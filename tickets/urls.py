from django.urls import path
from .views import ticket_list, ticket_detail, new_ticket

urlpatterns = [
    path("", ticket_list, name="ticket_list"),
    path("new/", new_ticket, name="new_ticket"),
    path("<int:ticket_id>/", ticket_detail, name="ticket_detail"),
]
