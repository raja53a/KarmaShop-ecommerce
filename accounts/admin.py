from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Accounts
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email','username','last_login','date_joined','is_active','is_admin')
    list_display_links = ('email','username')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Accounts,AccountAdmin)