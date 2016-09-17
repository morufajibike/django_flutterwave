
from django.conf.urls import include, url

import charge_card
import tokenize_card
import enquiry

charge_card_urls = [
    url(r'^initiate', charge_card.initiate, name="char_initiate"),
    url(r'^enter-otp', charge_card.enter_otp, name="char_enter_otp"),
    url(r'^transaction-result', charge_card.transaction_result, name="char_transaction_result"),
]

tokenize_card_urls = [
    url(r'^initiate', tokenize_card.initiate, name="tok_initiate"),
    url(r'^enter-otp', tokenize_card.enter_otp, name="tok_enter_otp"),
    url(r'^transaction-result', tokenize_card.transaction_result, name="tok_transaction_result"),
]

enquiry_urls = [
        url(r'^initiate', enquiry.initiate_bal_enquiry, name="initiate_bal_enquiry"),
        url(r'^get-available-banks', enquiry.get_available_banks, name="get_available_banks"),
        url(r'^account-enquiry', enquiry.account_enquiry, name="account_enquiry"),
]

urlpatterns = [
    url(r'^charge-card/', include(charge_card_urls)),
    url(r'^tokenize-card/', include(tokenize_card_urls)),
    url(r'^enquiry/', include(enquiry_urls)),
    
]
