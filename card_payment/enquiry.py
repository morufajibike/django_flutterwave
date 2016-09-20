from django.shortcuts import render, redirect
from flutterwave import Flutterwave
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
import requests, hashlib, base64
from Crypto.Cipher import DES3

from general import flw, api_key, merchant_key, generate_ref_no, keep_values, clear_values_from_session,\
                    get_countries, get_currencies


def keep_values(request, keys_list, data_dict):
    for key in keys_list:
        request.session[key] = data_dict[key]

def clear_values_from_session(request, keys_list):
    for key in keys_list:
        if request.session.has_key(key):
            del request.session[key]
            
            
            
def initiate_bal_enquiry(request):
    '''Verify'''
    
    if request.method == "POST":
        #print request.POST
        print 'posting to verify card'
                
        payload = request.POST.copy()
        #payload.update({"customerID": "cust1471629671",
        #            'responseUrl': reverse('payment:tok_initiate')})
        payload.pop('csrfmiddlewaretoken')
        
        
        #print 'data: ',data
        
        verify                  = flw.card.balanceEnquiry(payload)
        verify_json             = verify.json()
        
        #print 'verify_json: ',verify_json
        response_data = verify_json['data']
        
        if response_data.has_key('responsemessage'):
            responseMessage         = response_data['responsemessage']
            if responseMessage == None:
                response_data.update({'country': payload['country'], 'otptransactionidentifier': payload['transactionRef'],
                                      'transactionRef': payload['transactionRef']})
                #print 'response_data: ',response_data
                keys_list = ['otptransactionidentifier', 'transactionRef', 'country']
                keep_values(request, keys_list, response_data)
                return redirect(reverse('enter_otp'))
                
                
            messages.error(request, '%s' %responseMessage)
        
        else:
            responseMessage = verify_json['status']
            messages.error(request, '%s' %responseMessage)
            
    months = []
    for i in range(1, 13):
        months.append(str(i).zfill(2))
    
    years = []
    for i in range(6):
        years.append(str(2016+i))
    
    transactionRef = generate_ref_no()
    return render(request, 'enquiry/initiate.html', {'months': months, 'years': years, 'transactionRef': transactionRef,
                                                     'countries': get_countries()})
    
    



def fetch_available_banks():
    # endpoint = "http://staging1flutterwave.co:8080/pwc/rest/fw/banks/"
    # 
    # response = requests.post(endpoint).json()
    response                   = flw.bank.list()
    return response.json()
    
def get_available_banks(request):
    response = fetch_available_banks()
    #if response['status'] == 'success':
                
    return render(request, 'result.html', {'data': response['data'].iteritems(), 'bank_enquiry': 'bank_enquiry',
                                               })
        
    #return JsonResponse({'response': response['status']})


def account_enquiry(request):
    if request.method == "POST":
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken')
        data.update({'merchantid': merchant_key})
        
        #print 'data: ',data

        verify                  = flw.account.lookup(data)
        response             = verify.json()
        # endpoint = 'http://staging1flutterwave.co:8080/pwc/rest/pay/resolveaccount'
        # rp = request.POST.copy()
        # rp.pop('csrfmiddlewaretoken')
        # 
        # payload = {'destbankcode': encryption(api_key, rp['destbankcode']),
        #            'recipientaccount': encryption(api_key, rp['recipientaccount']),
        #            'merchantid': merchant_key}
        # 
        # print 'payload: ',payload
        # response = requests.post(endpoint, json=payload).json()
                
        return JsonResponse({'response': response})
            
    response = fetch_available_banks()
    return render(request, 'enquiry/account_enquiry.html', {'data': response['data'].iteritems()})
