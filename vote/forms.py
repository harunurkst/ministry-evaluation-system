from django import forms

from vote.models import Ministry, Area


class MinistrySelectForm(forms.Form):
    ministry = forms.ModelChoiceField(queryset=Ministry.objects.all())


class UserLoginForm(forms.Form):
    nid_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class VoteReportForm(MinistrySelectForm):
    year = forms.IntegerField()
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False)