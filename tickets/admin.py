from django.contrib import admin
from .models import Status, Ticket, Case

admin.site.register(Status)
admin.site.register(Ticket)
admin.site.register(Case)
