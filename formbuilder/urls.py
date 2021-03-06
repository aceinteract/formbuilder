"""formbuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib.auth import views
from django.views.static import serve

import os.path

assets = os.path.join(
    os.path.dirname(__file__), 'assets'
)

urlpatterns = [
    url(r'^', include('formbuilder_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^assets/(?P<path>.*)$', serve, {'document_root': assets}),
]
