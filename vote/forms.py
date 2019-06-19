from django import forms

from vote.models import Ministry, Area


class MinistrySelectForm(forms.Form):
    ministry = forms.ModelChoiceField(queryset=Ministry.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Ministry'}))


class UserLoginForm(forms.Form):
    nid_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NID number'}))
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}))


class VoteReportForm(MinistrySelectForm):
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}))
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Area'}))