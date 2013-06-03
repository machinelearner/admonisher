from django import forms

class DefaulterUploadForm(forms.Form):
    file  = forms.FileField(required=True)
    message = forms.CharField(required=True)
    from_number = forms.CharField(required=True)

