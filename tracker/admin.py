from django.contrib import admin
from .models import Account, BugTicket
from django.contrib.auth.admin import UserAdmin

# Code Citation: https://www.youtube.com/
# watch?v=XJU9vRARkGo&list=PLgCYzUzKIBE_dil025VAJnDjNZHHHR9mW&index=13
admin.site.register(BugTicket)


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'display_name', 'date_joined',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username', 'display_name', 'age')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
