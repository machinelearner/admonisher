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
                employee_id_phone_hash[id] = self.DEFAULT_INVALID_NUMBER
        return employee_id_phone_hash

    @classmethod
    def removeNonAscii(self,text): return "".join(filter(lambda x: ord(x)<128, text))

    def __unicode__(self):
        return unicode(self.employee_id)

