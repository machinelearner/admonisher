from django.db import models
from django.contrib.auth.models import User

class APIToken(models.Model):
    # TODO validate token and sid
    token  = models.CharField(max_length=41,null=False)
    sid = models.CharField(max_length=20,null=False)
    BASE_URL = "https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Sms/send"
    user = models.ForeignKey(User)
    class Meta:
        app_label = 'exotel'

    def get_url(self):
        return self.BASE_URL %(self.sid,self.token,self.sid)
