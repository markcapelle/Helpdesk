from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    title = models.TextField()

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tickets"
    )

    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    outcome = models.TextField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets"
    )

    def __str__(self):
        return self.title


class Case(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="cases"
    )

    created_at = models.DateField(auto_now_add=True)

    logged_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logged_cases"
    )

    body = models.TextField()

    hours = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Case #{self.id} for Ticket #{self.ticket.id}"
