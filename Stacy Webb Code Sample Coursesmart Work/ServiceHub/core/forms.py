__version__ = '1.0.0'
__author__ = 'Stacy E. Webb'


from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from util.CSService import CSService

csService = CSService('http://csrel.bvdep.com')

SERVICE_CHOICES = (
        ('admin', "CSAdmin"),
        ('viewebook', "ViewEBook"),
        ('viewbookshelf', 'ViewBookshelf'),
        ('cleardata', 'ClearCSData'),
)

class CSServiceForm(forms.Form):
    service = forms.ChoiceField(choices=SERVICE_CHOICES)
    user_id = forms.CharField(max_length=64, required=False)
    context_label = forms.CharField(max_length=64, required=False)
    lis_person_contact_email_primary = forms.CharField(max_length=128, required=False)
    roles = forms.CharField(max_length=64, required=False)
    
def requestService(request):
    if request.method == 'POST':
        form = CSServiceForm(request.POST)
        if form.is_valid():
            # process service//
            return HttpResponseRedirect('/requester/')
    else:
        form = CSServiceForm()
        
    return render_to_response('core/service_request.html',
                              {'form': form})