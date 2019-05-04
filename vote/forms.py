from django import forms

from vote.models import Ministry


class MinistrySelectForm(forms.Form):
    ministry = forms.ModelChoiceField(queryset=Ministry.objects.all())


class UserLoginForm(forms.Form):
    nid_number = forms.CharField()
    mobile_number = forms.CharField()