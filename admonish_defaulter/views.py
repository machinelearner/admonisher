from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from admonish_defaulter.forms import DefaulterUploadForm
from admonish_defaulter.models import DefaulterAction
from contacts.models import Contact, LDAPSearchParameters, LDAPToken
from exotel.models import SMSSender,APIToken
import logging
logger = logging.getLogger(__name__)

@login_required
def upload_defaulter_excel_sheet(request):
    if request.method == 'POST':
        form = DefaulterUploadForm(request.POST, request.FILES)
        if form.is_valid() and LDAPToken.exists() and LDAPSearchParameters.exists():
            list_of_defaulter_id = DefaulterAction.extract_defaulter_ids_from_excel(request.FILES['file'])
            message = request.POST['message']
            from_number = request.POST['from_number']
            defaulter_phone_hash = Contact.get_phone_number_for_defaulters(list_of_defaulter_id)
            send_sms_to_defaulters(request.user,from_number,defaulter_phone_hash,message)
            return HttpResponseRedirect('/')
        else:
            logger.error("Please check LDAP Token and Search parameters!!")
            return HttpResponseRedirect('/')
    else:
        form = DefaulterUploadForm()
    return render_to_response('defaulter_upload.html', {'form': form}, RequestContext(request))


def send_sms_to_defaulters(user,from_number,defaulter_phone_hash,message):
    api_token = APIToken.objects.filter(user=user)
    if not api_token:
        logger.error("No API TOKEN Associated with authenticated user!! Messages not sent")
        return
    api_token = api_token[0]
    sms_sender = SMSSender(from_number,api_token)
    for defaulter_id,phone in defaulter_phone_hash.iteritems():
        if phone != Contact.DEFAULT_INVALID_NUMBER:
            response_message = sms_sender.send_one(phone,message)
            logger.debug(response_message)
        else:
            logger.error("Could not find mobile number for %s!!!! Message not sent" %(defaulter_id))

