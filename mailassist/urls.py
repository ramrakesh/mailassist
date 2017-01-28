"""mailassist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

urlpatterns = [
    
    # Core Main
    url(r'^', include('core.urls')),

    # User Main
    url(r'^user/', include('users.urls')),

    # Login
    url(r'^login/', include('core.urls')), 

    # Logout
    url(r'^user/logout/', include('core.urls')),
    
    # Gmail Callback
    url(r'^gmailCallback/', include('core.urls')),

    # APIs
    url(r'^user/api/user/', include('users.urls')), # For User APIs

    # Plugin APIs
    url(r'^plugin/api/', include('core.urls')),
    url(r'^user/plugin/api/', include('users.urls')),

    url(r'^admin/', include(admin.site.urls))
]
