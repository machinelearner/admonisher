from django.contrib import admin
from exotel.models import APIToken

class APITokenAdmin(admin.ModelAdmin):
    fields = ['token', 'sid','user']
    list_display = ('token', 'sid','user')

admin.site.register(APIToken,APITokenAdmin)

