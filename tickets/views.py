from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Status, Case, User
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime, date, timedelta
from django.http import JsonResponse


@permission_required('tickets.view_ticket', raise_exception=True)
@login_required
def ticket_list(request):

    status_filter = request.GET.get("status", "open")
    assigned_filter = request.GET.get("assigned", "all")
    sort = request.GET.get("sort", "")

    # Base queryset
    if status_filter == "all":
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(
            status__name__iexact=status_filter
        )

    # Assigned-to filter
    if assigned_filter != "all":
        tickets = tickets.filter(assigned_to__id=assigned_filter)

    # Sorting map
    sort_map = {
        "title_asc": "title",
        "title_desc": "-title",
        "created_asc": "created_at",
        "created_desc": "-created_at",
        "due_asc": "due_date",
        "due_desc": "-due_date",
    }

    # Apply sorting
    if sort in sort_map:
        tickets = tickets.order_by(sort_map[sort])
    else:
        tickets = tickets.order_by("created_at")

    statuses = Status.objects.all()
    users = User.objects.all().order_by("username")

    return render(request, "tickets/ticket_list_view.html", {
        "tickets": tickets,
        "statuses": statuses,
        "users": users,
        "status_filter": status_filter,
        "assigned_filter": assigned_filter,
        "sort": sort,
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


        # Save ticket fields
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

        # Save Cases (existing + new)
        from .models import Case

        for key, value in request.POST.items():

            # Only process case bodies
            if not key.startswith("case_body_"):
                continue

            case_id = key.replace("case_body_", "")
            body = value.strip()
            hours_raw = request.POST.get(f"case_hours_{case_id}", "").strip()

            # Skip completely empty cases
            if not body and not hours_raw:
                continue

            # Convert hours
            hours = None
            if hours_raw:
                try:
                    hours = float(hours_raw)
                except ValueError:
                    hours = None

            # NEW CASE
            if case_id.startswith("new"):
                Case.objects.create(
                    ticket=ticket,
                    body=body,
                    hours=hours,
                    logged_by=request.user
                )
                continue

            # EXISTING CASE
            try:
                case = Case.objects.get(id=case_id, ticket=ticket)
            except Case.DoesNotExist:
                continue

            case.body = body
            case.hours = hours
            case.save()

        # AJAX Save & Close
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"saved": True})

    return render(request, "tickets/ticket_detail.html", {
        "ticket": ticket,
        "assignable_users": assignable_users,
        "statuses": statuses,
        "current_username": request.user.username,
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



@permission_required('tickets.delete_ticket', raise_exception=True)
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        ticket.delete()
        return redirect("ticket_list")

    return render(request, "tickets/confirm_delete_ticket.html", {
        "ticket": ticket
    })




@permission_required('tickets.delete_case', raise_exception=True)
@login_required
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    ticket_id = case.ticket.id

    if request.method == "POST":
        case.delete()
        return redirect("ticket_detail", ticket_id=ticket_id)

    return render(request, "tickets/confirm_delete_case.html", {
        "case": case,
        "ticket_id": ticket_id
    })
