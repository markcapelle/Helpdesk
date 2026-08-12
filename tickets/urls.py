from django.urls import path
from .views import (
    ticket_list, ticket_detail, new_ticket,
    delete_ticket, delete_case
)

urlpatterns = [
    path("", ticket_list, name="ticket_list"),
    path("new/", new_ticket, name="new_ticket"),
    path("<int:ticket_id>/", ticket_detail, name="ticket_detail"),
    path("<int:ticket_id>/delete/", delete_ticket, name="delete_ticket"),
    path("case/<int:case_id>/delete/", delete_case, name="delete_case"),
]
