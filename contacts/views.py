from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from contacts.forms import ContactCSVUploadForm
from contacts.models import Contact

@login_required
def upload_contacts_csv(request):
    if request.method == 'POST':
        form = ContactCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            Contact.insert_contacts_from_csv(request.FILES['file'])
            return HttpResponseRedirect('/admin/contacts/contact/')
    else:
        form = ContactCSVUploadForm()
    return render_to_response('upload.html', {'form': form}, RequestContext(request))
