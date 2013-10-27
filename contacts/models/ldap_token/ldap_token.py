import json
from django.db import models
import ldap, time, re

class LDAPToken(models.Model):
    server_ip = models.CharField(max_length=20, null=False)
    auth_credential = models.CharField(max_length=200, null=False)
    password = models.CharField(max_length=100, null=False)
    ldap_connection = None

    class Meta:
        app_label = 'contacts'


    def establish_connection(self):
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
            ldap_connection = ldap.initialize(self.server_ip, trace_level=1)
            ldap_connection.simple_bind_s(self.auth_credential, self.password)
            time.sleep(0.5)  #wait for AD to authenticate
            self.ldap_connection = ldap_connection
        except ldap.LDAPError, e:
            print e

    def get_other_mobile_for_id(self, uid_number, search_parameters):
        print "####################", uid_number, "       ", search_parameters
        base_dn = search_parameters.base_dn
        search_scope = search_parameters.search_scope
        search_filter = search_parameters.search_filter + "=%s" % (uid_number)
        retrieve_attributes = search_parameters.retrieve_attributes
        self.establish_connection()
        ldap_result_id = self.ldap_connection.search(base_dn, int(search_scope), search_filter,
            [str(retrieve_attributes)])
        time.sleep(0.2) #wait for AD to return
        result_type, result_data = self.ldap_connection.result(ldap_result_id, 0)
        result_list = []
        try:
            if(result_data):
                result_list = result_data[0][1]['otherMobile']
                result_list = map(lambda x: self.get_valid_number(x), result_list)
        except KeyError:
            pass
        return result_list

    def get_valid_number(self, number_string):
        return ''.join([char for char in number_string if re.match('(\+|\d)', char)])


    def __unicode__(self):
        return unicode(self.server_ip)

    @classmethod
    def exists(self):
        try:
            ldap_token = self.objects.get()
            return True
        except:
            return False
