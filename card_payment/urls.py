
from django.conf.urls import include, url

import views

urlpatterns = [
    
    url(r'^initiate', views.initiate, name="initiate"),
    url(r'^enter-otp', views.enter_otp, name="enter_otp"),
    url(r'^validation-result', views.validation_result, name="validation_result"),

]
