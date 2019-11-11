"""Swoosh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from myWebsite import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.login),
    url(r'^identify/$', views.identify),
    url(r'^comgoods/$', views.comgoods),
    url(r'^cuslist/$', views.cuslist),
    url(r'^goodlist/$', views.goodlist),
    url(r'^system/$', views.system),
    url(r'^cussta/$', views.cussta),
    url(r'^tralist/$', views.tralist),
    url(r'^uptrade/$', views.uptrade),
    url(r'^userreg/$', views.userreg),
    url(r'^classgoods/$', views.classgoods),
    url(r'^recom/$', views.recom),
    url(r'^predict/$', views.predict)
]
