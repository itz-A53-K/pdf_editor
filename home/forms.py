from django import forms

class fileInp_frm(forms.Form):
    # file= forms.FileField( widget=forms.ClearableFileInput(attrs={"multiple": True, 'accept':".pdf"}))
    file= forms.FileField( widget=forms.ClearableFileInput({'accept':'.pdf'}))
