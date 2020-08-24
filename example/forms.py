from django import forms


class ToastForm(forms.Form):
    message = forms.CharField()
    sleep_time = forms.IntegerField()
