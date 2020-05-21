from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegistrationForm, LoginForm, AddTicketForm
from .models import Account, BugTicket


@login_required
def index(request):
    tickets = BugTicket.objects.all()
    return render(request, 'index.html', {'tickets': tickets})


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
