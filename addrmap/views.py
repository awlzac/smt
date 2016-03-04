from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.forms.models import model_to_dict
import json
from addrmap import forms
from addrmap.models import Address
from addrmap import fusion_access

SM_INVREQ = "Invalid request"

def json_response(status, message):
    '''
    Return a json response. For this app, the default json response 
    is the status and message, and the current address list.
    '''
    try:
        data = [model_to_dict(ad) for ad in Address.objects.all()]
    except Exception as e:
        status = 500
        message = str(e)
    
    return HttpResponse(content=json.dumps(data),
                        status=status, 
                        reason=message,
                        content_type="application/json") 

def collect_errors(f):
    '''
    help function to collect error text from a form that is not valid.
    '''
    return ''.join([''.join(e) for e in f.errors.values()])

def index(request):
    '''
    View for the single-page app; initial data passed in here, 
    template handles everything else.
    '''
    datadict= {'tablekey': fusion_access.tablekey,
               'apikey': fusion_access.apikey}
    return render_to_response('addrmap/index.html.t',
                              RequestContext(request, datadict))
       
def address_get(request):
    '''
    Ajax/data view; do nothing and return current address list.
    '''
    return json_response(200, '')

def address_add(request):
    '''
    Ajax view; client posts here to add an address.
    '''
    if request.method != 'POST':
        # shouldn't be here - reroute to index
        return HttpResponseRedirect(reverse('addrmap:index'))
    status = 400
    message = SM_INVREQ
    try:
        f = forms.AddressForm(request.POST)
        if f.is_valid():
            desc = f.cleaned_data['desc']
            lng = f.cleaned_data['lng']
            lat = f.cleaned_data['lat']
            newaddr = Address(desc=desc, lng=lng, lat=lat)
            newaddr.save()
            # add to fusion as well
            fusion_access.add_to_fusion(newaddr)
            
            status = 200
            message = "added "+desc
        else:
            # errors in submitted data
            message = collect_errors(f)
    except Exception as e:
            message = str(e)
            status = 500
    return json_response(status, message)

def address_trunc(request):
    '''
    Ajax view; client posts here to clear all addresses from the system.
    '''
    if request.method != 'POST':
        # shouldn't be here - reroute to index
        return HttpResponseRedirect(reverse('addrmap:index'))
    status = 400
    message = SM_INVREQ
    try:
        ct = Address.objects.count()
        Address.objects.all().delete()
        # trunc fusion as well
        fusion_access.trunc_fusion()
        
        status = 200
        message = "deleted {} addresses".format(ct)
    except Exception as e:
        message = str(e)
        status = 500    
    return json_response(status, message)