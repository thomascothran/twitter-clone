"""twitter_clone URL Configuration

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

from . import views

urlpatterns = [
    url(r'^create-entry/', views.BlogEntryCreate.as_view(), name="create_entry"),
    url(r'^entry/(?P<pk>\d+)/$', views.BlogEntryDetail.as_view(), name="entry_detail"),
    url(r'^user/(?P<pk>\d+)/$', views.UserProfile.as_view(), name='user_profile'),
    url(r'^user-list/$', views.UserList.as_view(), name='user_list'),
]
