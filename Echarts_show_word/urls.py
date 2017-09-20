"""Echarts_show_word URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from graph import views as page

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', page.nanke, name = 'home'),
    url(r'^fuke', page.fuke, name='fuke'),
    url(r'^nanke', page.nanke, name='nanke'),
    url(r'^obesity', page.obesity, name='obesity'),
    url(r'^skin', page.skin, name='skin'),
    url(r'^note', page.note, name = 'note'),
    url(r'^add_note', page.add_note, name = 'add_note'),
]
