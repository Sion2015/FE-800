"""CGM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('home.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^start/', include('start.urls')),
    url(r'^questionnaire/', include('questionnaire.urls')),
    url(r'^risk_tolerance/', include('risk_tolerance.urls')),

    url(r'^show_plan/', include('show_plan.urls')),
    url(r'^management/', include('management.urls')),
    # url(r'^still_working/', include('still_working.urls')),
    url(r'^management_form_1/', include('management_form_1.urls')),
    url(r'^management_form_2/', include('management_form_2.urls')),
    url(r'^management_form_3/', include('management_form_3.urls')),
    url(r'^management_form_4/', include('management_form_4.urls')),
    url(r'^confirmation/', include('confirmation.urls')),
    url(r'^management_reset/', include('management_reset.urls')),
    url(r'^management_step_1/', include('management_step_1.urls')),
    url(r'^management_step_2/', include('management_step_2.urls')),
    url(r'^management_step_3/', include('management_step_3.urls')),
    url(r'^management_step_4/', include('management_step_4.urls')),
    url(r'^management_step_5/', include('management_step_5.urls')),
    url(r'^management_step_6/', include('management_step_6.urls')),


]
