from django.conf.urls import url

from questionnaire import views

urlpatterns = [
    url(r'^$', views.questionnaire, name='questionnaire'),
]