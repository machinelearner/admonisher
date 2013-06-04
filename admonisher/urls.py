from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from contacts.views import upload_contacts_csv
from admonish_defaulter.views import upload_defaulter_excel_sheet

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'admonisher.views.home', name='home'),
    # url(r'^admonisher/', include('admonisher.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),

    ######                      ######
    #   Application specific URLs    #
    ######                      ######
    #url(r'',)
    url(r'^$', RedirectView.as_view(url= 'defaulter/excel_upload')),
    url(r'^contacts/csv_upload$', upload_contacts_csv),
    url(r'defaulter/excel_upload',upload_defaulter_excel_sheet),

)
urlpatterns += staticfiles_urlpatterns()
