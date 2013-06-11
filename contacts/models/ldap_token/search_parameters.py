from django.db import models

class LDAPSearchParameters(models.Model):
    # TODO validate token and sid
    base_dn = models.CharField(max_length=100,null=False)
    search_scope = models.CharField(max_length=200,null=False,default=2)
    search_filter = models.CharField(max_length=100,null=False)
    retrieve_attributes = models.CharField(max_length=100,null=False)

    class Meta:
        app_label = 'contacts'

    @classmethod
    def exists(self):
        try:
            search_parameters = self.objects.get()
            return True
        except:
            return False


