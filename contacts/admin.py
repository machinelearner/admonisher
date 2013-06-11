from django.contrib import admin
from contacts.models import Contact,LDAPToken,LDAPSearchParameters

class ContactAdmin(admin.ModelAdmin):
    fields = ['employee_id','name','phone_number']
    list_display = ('employee_id','name','phone_number')
    search_fields = ['employee_id','name']

class LDAPTokenAdmin(admin.ModelAdmin):
    fields = ['server_ip','password','auth_credential']
    list_display = ('auth_credential','server_ip',)
    search_fields = ['server_ip','auth_credential']

class LDAPSearchParameterAdmin(admin.ModelAdmin):
    fields = ['base_dn','search_scope','search_filter','retrieve_attributes']
    list_display = ('base_dn','search_scope','search_filter',)
    search_fields = ['base_dn','search_scope','search_filter','retrieve_attributes']

admin.site.register(Contact,ContactAdmin)
admin.site.register(LDAPToken ,LDAPTokenAdmin)
admin.site.register(LDAPSearchParameters ,LDAPSearchParameterAdmin)
