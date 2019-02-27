"""varos URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="registration/password_reset_confirm.html"),
        name='password_reset_confirm'),
        
    url(r'^api/v1/admin/', include('rest_auth.urls')),
    url(r'^api/v1/admin/',include('admin_user.urls')),

    url(r'^api/v1/customers/', include('rest_auth.urls')),
    url(r'^api/v1/customers/',include('customer_user.urls')),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),

    url(r'^api/v1/admin/users/groups/',include('user_group.urls')),

    path('admin/', admin.site.urls),
    url(r'^api/v1/admin/',include('admin_user.urls')),
]
