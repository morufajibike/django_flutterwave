
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from card_payment.general import enter_otp


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', TemplateView.as_view(template_name = 'options.html'), name="options"),
    url(r'^enter-otp', enter_otp, name="enter_otp"),
    url(r'^payment/', include('card_payment.urls', namespace="payment")),
]
