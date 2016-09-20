from flutterwave import Flutterwave

from django.conf import settings
import random
from django.shortcuts import render, redirect
import ast
from django.contrib import messages
from django.core.urlresolvers import reverse



def keep_values(request, keys_list, data_dict):
    for key in keys_list:
        request.session[key] = data_dict[key]

def clear_values_from_session(request, keys_list):
    for key in keys_list:
        if request.session.has_key(key):
            del request.session[key]


api_key         = settings.FLUTTERWAVE_API_KEY
merchant_key    = settings.FLUTTERWAVE_MERCHANT_KEY

def initialize_flw(api_key, merchant_key):    
    flw = Flutterwave(api_key, merchant_key, {"debug": True})
    return flw

flw  = initialize_flw(api_key, merchant_key)

def generate_ref_no():
    ref_no = ''
    digits = '1234567890'
    ref_no_length = 9
    for x in range(ref_no_length):
        ref_no += digits[random.randint(0, len(digits) - 1)]
    return ref_no

def return_data(data_dict):
    dataList = []
    for key, val in data_dict.iteritems():
        dataList.append({'code': key, 'name': val['name']})
    return dataList

def get_countries():
    data_dict = flw.util.countryList()
    return return_data(data_dict)

def get_currencies():
    data_dict = flw.util.currencyList()
    return return_data(data_dict)

def enter_otp(request):
    rG = request.GET
    if rG.has_key('resp'):
        
        response_data = ast.literal_eval(rG['resp'])
        responsemessage = response_data['responsemessage']
        messages.error(request, '%s' %responsemessage)
        print "request.META.get('HTTP_REFERER'): ",request.META.get('HTTP_REFERER')
        return redirect(request.META.get('HTTP_REFERER'))
        #return redirect(reverse('payment:char_initiate'))
    
    if request.session.has_key('otptransactionidentifier'):# and request.session.has_key('verifyUsing'):
        context = {'otpTransactionIdentifier': request.session['otptransactionidentifier'],
                   'country': request.session['country']}
        return render(request, 'enter_otp.html', context)
    
    return redirect(reverse('options'))
