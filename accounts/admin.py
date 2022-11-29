from django.contrib import admin
from . models import Account,UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Messages

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src ="{}" width = "30" style = "border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_discription = 'profile Picture'
    list_display = ('user', 'city', 'state', 'country','thumbnail')
class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','last_login','is_active','date_joined')
    list_display_links=('email','first_name','last_name')
    ordering=('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Messages)