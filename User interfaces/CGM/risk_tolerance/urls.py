from django.conf.urls import url

from risk_tolerance import views

urlpatterns = [
    url(r'^$', views.risk_tolerance, name='risk_tolerance'),
]