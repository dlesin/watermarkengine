from django import forms


class FileFieldForm(forms.Form):
    text_field = forms.CharField(max_length=50)
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

