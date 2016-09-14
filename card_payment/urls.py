
from django.conf.urls import include, url
from django.views.generic import TemplateView

import charge_card
import tokenize_card

charge_card_urls = [
    url(r'^initiate', charge_card.initiate, name="initiate"),
    url(r'^enter-otp', charge_card.enter_otp, name="enter_otp"),
    url(r'^transaction-result', charge_card.transaction_result, name="transaction_result"),
]

tokenize_card_urls = [
    url(r'^initiate', tokenize_card.initiate, name="initiate"),
    url(r'^enter-otp', tokenize_card.enter_otp, name="enter_otp"),
    url(r'^transaction-result', tokenize_card.transaction_result, name="transaction_result"),
]

urlpatterns = [
    url(r'^options/$', TemplateView.as_view(template_name = 'options.html'), name="options"),
    url(r'^charge-card/', include(charge_card_urls)),
    #url(r'^tokenize-card/', include(tokenize_card_urls)),
]
