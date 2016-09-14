from django.shortcuts import render, redirect
from flutterwave import Flutterwave
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

api_key         = "tk_HhfBSYgKZwid1E8G9yPF"
merchant_key    = "tk_biDdQrtXvO"

def initialize_flw(api_key, merchant_key):    
    flw = Flutterwave(api_key, merchant_key, {"debug": True})
    return flw

def keep_values(request, keys_list, data_dict):
    for key in keys_list:
        request.session[key] = data_dict[key]

def clear_values_from_session(request, keys_list):
    for key in keys_list:
        if request.session.has_key(key):
            del request.session[key]
            
            
def initiate(request):
    '''Verify'''
    
    if request.method == "POST":
        print request.POST
        print 'posting to verify card'
                
        payload = request.POST.copy()
        payload.update({"customerID": "cust1471629671",
                    'responseUrl': reverse('payment:initiate')})
        payload.pop('csrfmiddlewaretoken')
        
        bvn_or_pin = False
        if payload['authModel'] == ('BVN' or 'PIN'):
            bvn_or_pin = True
        
        flw                     = initialize_flw(api_key, merchant_key)
        #print 'data: ',data
        
        verify                  = flw.card.charge(payload)
        verify_json             = verify.json()
        
        print 'verify_json: ',verify_json
        response_data = verify_json['data']
        
        if response_data.has_key('responsemessage'):
            responseMessage         = response_data['responsemessage']
            messages.error(request, '%s' %responseMessage)
        
        if verify_json['status'] != 'error':
            
            response_data.update({'country': payload['country']})
            print 'response_data: ',response_data
            responsecode = response_data['responsecode']
            if responsecode == '02':
                keys_list = ['otptransactionidentifier', 'transactionreference', 'country']
                keep_values(request, keys_list, response_data)
                
                if bvn_or_pin == True:
                    return redirect(reverse('payment:enter_otp'))
        else:
            responseMessage = verify_json['status']
            messages.error(request, '%s' %responseMessage)
            
    months = []
    for i in range(1, 13):
        months.append(str(i).zfill(2))
    
    years = []
    for i in range(6):
        years.append(str(2016+i))
    
    return render(request, 'initiate.html', {'months': months, 'years': years})
    


def enter_otp(request):
    
    if request.method == 'POST':
        data = request.POST.copy()
        
        flw                     = initialize_flw('', '')
        
        verify                  = flw.card.validate(data)
        verify_json             = verify.json()
        
        
    else:
        if request.session.has_key('otptransactionidentifier'):# and request.session.has_key('verifyUsing'):
            context = {'otpTransactionIdentifier': request.session['otptransactionidentifier'],
                       'country': request.session['country']}
            return render(request, 'enter_otp.html', context)
        
        return redirect(reverse('initiate'))

def validation_result(request):
    # context = {}
    # '''Validate BVN'''
    # if request.method == "POST":
    #     otp = request.POST.get('otp')
    #     
    #     '''Retrieve saved values from session'''
    #     api_key, merchant_key, verifyUsing, country, transactionReference, bvn  = retrieve_values(request)           
    #     
    #     flw                                     = initialize_flw(api_key, merchant_key)
    #     validate                                = flw.bvn.validate(bvn, otp, transactionReference, country)
    #     validate_json                           = validate.json()
    #     
    #     print 'validate_json: ',validate_json
    #     
    #     context.update({'data': validate_json['data']})
    #             
    #     # '''Clear saved values from session'''
    #     keys_list = ['api_key', 'merchant_key', 'verifyUsing', 'country', 'transactionReference', 'bvn']
    #     clear_values_from_session(request, keys_list)

        
    return render(request, 'bvn/bvn_verification_result.html', context)
        
    