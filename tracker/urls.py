from django.urls import path
from tracker import views

urlpatterns = [
    path('',
         views.index,
         name='homepage'),
    path('bug-ticket/<int:pk>',
         views.BugTicketDetailView.as_view(),
         name='bug-ticket-detail'),
    path('accounts/<int:pk>',
         views.AccountDetailView.as_view(),
         name='account-detail'),
    path('register/',
         views.registration_view,
         name='register'),
    path('logout/',
         views.logoutview,
         name='logout'),
    path('login/',
         views.loginview,
         name='login'),
    path('ticket-add/',
         views.ticketadd,
         name='ticket-add'),
    path(
        'ticket/edit/<int:id>',
        views.ticket_edit,
        name='ticket-edit'
    ),
    path('ticket-invalid/<int:id>',
         views.mark_ticket_invalid,
         name='ticket-invalid'
         ),
    path('ticket-new/<int:id>',
         views.mark_ticket_new,
         name='ticket-new'
         ),
    path('ticket-assign-self/<int:id>',
         views.assign_ticket_self,
         name='assign-ticket-self')
]
