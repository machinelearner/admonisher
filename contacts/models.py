from django.db import models
from csv import DictReader

class Contact(models.Model):
    # TODO validate token and sid
    employee_id = models.CharField(max_length=5,null=False)
    name = models.CharField(max_length=200,null=False)
    phone_number = models.CharField(max_length=10,null=False)

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
    def removeNonAscii(self,text): return "".join(filter(lambda x: ord(x)<128, text))

    def __unicode__(self):
        return unicode(self.employee_id)

