"""redcap_rest URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'redcap_rest'
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
 	url(r'^redcap_rest/getforms$', views.getforms, name='getforms'),
 	url(r'^redcap_rest/results/(?P<record_id>[0-9]+)$', views.results, name='results'),
	url(r'^redcap_rest/detail$', views.detail, name='detail'), 	
	url(r'^redcap_rest/authorize$', views.authorize, name='authorize'), 	
 	#url(r'^redcap_rest/person/(?P<record_id>[0-9]+)$', views.person, name='person'),	
	url(r'^redcap_rest/personinfo/$', views.personinfo, name='personinfo'),	 	
	url(r'^redcap_rest/mrns/$', views.mrns, name='mrns'),
	url(r'^redcap_rest/add/$', views.add, name='add'),	 			
	url(r'^save/$', views.save, name='save'),	
]
