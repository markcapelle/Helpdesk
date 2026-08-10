from django.shortcuts import render, get_object_or_404
from .models import Ticket, Status
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta


@permission_required('tickets.view_ticket', raise_exception=True)
@login_required
def ticket_list(request):
    status_filter = request.GET.get("status", "open")

    if status_filter == "all":
        tickets = Ticket.objects.all().order_by("created_at")
    else:
        tickets = Ticket.objects.filter(
            status__name__iexact=status_filter
        ).order_by("created_at")

    statuses = Status.objects.all()

    return render(request, "tickets/ticket_list.html", {
        "tickets": tickets,
        "statuses": statuses,
        "status_filter": status_filter,
    })



@permission_required('tickets.change_ticket', raise_exception=True)
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Users in the "user" group
    from django.contrib.auth.models import Group
    user_group = Group.objects.get(name__iexact="user")
    assignable_users = user_group.user_set.all()

    # All statuses
    statuses = Status.objects.all().order_by("name")

    if request.method == "POST":
        ticket.title = request.POST.get("title")
        ticket.description = request.POST.get("description")
        ticket.outcome = request.POST.get("outcome")

        # Created date
        created_raw = request.POST.get("created_at")
        if created_raw:
            ticket.created_at = datetime.strptime(created_raw, "%Y-%m-%d").date()

        # Due date
        due_raw = request.POST.get("due_date")
        if due_raw:
            ticket.due_date = datetime.strptime(due_raw, "%Y-%m-%d").date()
        else:
            ticket.due_date = None

        # Assigned user
        assigned_id = request.POST.get("assigned_to")
        ticket.assigned_to = assignable_users.filter(id=assigned_id).first() if assigned_id else None

        # Status
        status_id = request.POST.get("status")
        ticket.status = statuses.filter(id=status_id).first() if status_id else ticket.status

        ticket.save()

    return render(request, "tickets/ticket_detail.html", {
        "ticket": ticket,
        "assignable_users": assignable_users,
        "statuses": statuses,
    })







@permission_required('tickets.add_ticket', raise_exception=True)
@login_required
def new_ticket(request):

    # Ensure default "open" status exists
    try:
        default_status = Status.objects.get(name__iexact="open")
    except Status.DoesNotExist:
        default_status = Status.objects.create(name="open")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Ticket.objects.create(
            title=title,
            description=description,
            status=default_status,
            assigned_to=request.user,
            due_date=date.today() + timedelta(days=7)
        )

        return redirect("ticket_list")

    return render(request, "tickets/new_ticket.html")