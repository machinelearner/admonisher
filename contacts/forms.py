from django import forms

class ContactCSVUploadForm(forms.Form):
    file  = forms.FileField()
