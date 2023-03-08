from django.shortcuts import render
from django.views.generic import TemplateView
from django import forms
from .constants import TEMPLATE_INDEX

class NameForm(forms.Form):
    your_name = forms.CharField(label='name')

class IndexView(TemplateView):
    '''Main page.'''
    template_name: str = TEMPLATE_INDEX
