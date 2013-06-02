from django.contrib import admin
from contacts.models import Contact

class ContactAdmin(admin.ModelAdmin):
    fields = ['employee_id','name','phone_number']
    list_display = ('employee_id','name','phone_number')
    search_fields = ['employee_id','name']

admin.site.register(Contact,ContactAdmin)
