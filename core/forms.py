from django import forms


class FileFieldForm(forms.Form):
    text_field = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control mt-1', 'placeholder': 'Ваш текст'}))
    file_field = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': True, 'class': 'custom-file-input input-files-js', 'lang': 'ru'}))
