from contacts.models import LDAPToken, LDAPSearchParameters
from django.db import models
from csv import DictReader
from collections import defaultdict

class Contact(models.Model):
    # TODO validate token and sid
    employee_id = models.CharField(max_length=5,null=False)
    name = models.CharField(max_length=200,null=False)
    phone_number = models.CharField(max_length=10,null=False)
    DEFAULT_INVALID_NUMBER = "9999999999"

    class Meta:
        app_label = 'contacts'

    @classmethod
    def insert_contacts_from_csv(self,csv_file):
        reader = DictReader(csv_file)
        for row in reader:
            mobile_number = self.removeNonAscii(row['mobile_number'])
            employee_id = self.removeNonAscii(row['employee_id'])
            name = self.removeNonAscii(row['employee_name'])
            print row
            self(employee_id=employee_id,name=name,phone_number=mobile_number).save()

    @classmethod
    def get_phone_number_for_defaulters(self,list_of_ids):
        #Think of a better option, dont fire too many queries
        employee_id_phone_hash = defaultdict(str)
        for id in list_of_ids:
            contacts = self.objects.filter(employee_id=id)
            if contacts:
                employee_id_phone_hash[id] = contacts[0].phone_number
            else:
                ldap_access = LDAPToken.objects.get()
                ldap_search_parameters = LDAPSearchParameters.objects.get()

                result_list = ldap_access.get_other_mobile_for_id(id, ldap_search_parameters)
                if not result_list:
                    employee_id_phone_hash[id] = Contact.DEFAULT_INVALID_NUMBER
                else:
                    employee_id_phone_hash[id] = result_list[0]
        return employee_id_phone_hash

    @classmethod
    def get_phone_numbers_from_active_directory(self,defaulter_id,ldap_token,search_parameters):
        phone_numbers = ldap_token.get_other_mobile_for_id(defaulter_id,search_parameters)
        return map(lambda number: Contact(name="TEMP_VARIABLE",employee_id=defaulter_id,phone_number=number),phone_numbers)

    @classmethod
    def removeNonAscii(self,text): return "".join(filter(lambda x: ord(x)<128, text))

    def __unicode__(self):
        return unicode(self.employee_id)


