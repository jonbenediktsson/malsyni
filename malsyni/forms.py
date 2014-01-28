# coding: utf-8
from django import forms

KYN =(('drengur', 'Drengur'), ('stulka', 'Stúlka'))

class Malsyniform(forms.Form):
    malsyni = forms.CharField(widget=forms.Textarea)
    aldur = forms.CharField()
    kyn = forms.ChoiceField(widget=forms.Select(), choices=KYN)
