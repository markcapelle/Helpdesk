from django.shortcuts import render, get_object_or_404
from .models import Ticket, Status
from django.shortcuts import render, redirect
from .models import Ticket, Status
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Status

def ticket_list(request):
    status_filter = request.GET.get("status", "open")

    if status_filter == "all":
        tickets = Ticket.objects.all().order_by("created_at")
    else:
        tickets = Ticket.objects.filter(status__name__iexact=status_filter).order_by("created_at")

    statuses = Status.objects.all()

    return render(request, "tickets/ticket_list.html", {
        "tickets": tickets,
        "statuses": statuses,
        "status_filter": status_filter,
    })


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})


@login_required
def new_ticket(request):
    # Get the default "open" status
    try:
        default_status = Status.objects.get(name__iexact="open")
    except Status.DoesNotExist:
        # Safety fallback: create it if missing
        default_status = Status.objects.create(name="open")

    if request.method == "POST":
        title = request.POST.get("title")

        Ticket.objects.create(
            title=title,
            status=default_status,
            assigned_to=request.user
        )

        return redirect("ticket_list")

    return render(request, "tickets/new_ticket.html")