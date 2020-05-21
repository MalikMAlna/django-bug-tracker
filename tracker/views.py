from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.detail import DetailView
from .forms import RegistrationForm, LoginForm, AddTicketForm
from .models import Account, BugTicket


@login_required
def index(request):
    tickets = BugTicket.objects.all()
    return render(request, 'index.html', {"tickets": tickets})


class BugTicketDetailView(DetailView):
    model = BugTicket
    context_object_name = 'bug_ticket'


class AccountDetailView(DetailView):
    model = Account
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['personal_bug_tickets'] = BugTicket.objects.all()
        return context


def loginview(request):
    html = 'login.html'
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password'],
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
        else:
            context['login_form'] = form
    else:
        form = LoginForm()
        context['login_form'] = form
    return render(request, html, context)


def logoutview(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect(reverse('homepage'))


@login_required
@staff_member_required
def registration_view(request):
    html = 'register.html'
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(
                username=username,
                password=raw_password
            )
            login(request, account)
            return HttpResponseRedirect(
                request.GET.get('next', reverse('homepage'))
            )
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, html, context)


@login_required
def ticketadd(request):
    html = 'genericform.html'
    form = AddTicketForm()
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            BugTicket.objects.create(
                title=data['title'],
                description=data['description'],
                creator=request.user
            )
            messages.info(request, "Ticket created successfully!")
            return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {"form": form})


@login_required
def ticket_edit(request, id):
    ticket = BugTicket.objects.get(id=id)
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data['title']
            ticket.description = data['description']
            ticket.save()
            return HttpResponseRedirect(
                reverse('bug-ticket-detail', args=(id,))
            )
    form = AddTicketForm(initial={
        'title': ticket.title,
        'description': ticket.description,
    })
    return render(request, "genericform.html", {"form": form})


@login_required
def mark_ticket_invalid(request, id):
    ticket = BugTicket.objects.get(id=id)
    ticket.ticket_status = "INV"
    ticket.save()
    return HttpResponseRedirect(
        reverse('bug-ticket-detail', args=(id,))
    )


@login_required
def mark_ticket_new(request, id):
    ticket = BugTicket.objects.get(id=id)
    ticket.ticket_status = "NEW"
    ticket.assigned_to = None
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(
        reverse('bug-ticket-detail', args=(id,))
    )


@login_required
def assign_ticket_self(request, id):
    ticket = BugTicket.objects.get(id=id)
    ticket.ticket_status = "INP"
    ticket.assigned_to = request.user
    ticket.save()
    return HttpResponseRedirect(
        reverse('bug-ticket-detail', args=(id,))
    )


@login_required
def mark_ticket_completed(request, id):
    ticket = BugTicket.objects.get(id=id)
    ticket.ticket_status = "DNE"
    ticket.completed_by = request.user
    ticket.save()
    return HttpResponseRedirect(
        reverse('bug-ticket-detail', args=(id,))
    )
