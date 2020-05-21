from django.urls import path
from tracker import views

urlpatterns = [
    path('',
         views.BugTicketListView.as_view(),
         name='homepage'),
    path('recipes/<int:pk>',
         views.BugTicketDetailView.as_view(),
         name='bug-ticket-detail'),
    path('authors/<int:pk>',
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
]
