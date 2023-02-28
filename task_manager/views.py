from django.shortcuts import render
from django.views import View
from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='name')

class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')
