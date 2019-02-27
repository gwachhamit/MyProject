from django.conf.urls import url
from customer_user import views
from django.urls import include

from .views import RegisterView
from allauth.account.views import confirm_email as allauthemailconfirmation

urlpatterns = [
    #overriding registration/account-confirm-email
    url(r"^registration/account-confirm-email/(?P<key>[\s\d\w().+-_',:&]+)/$",
    allauthemailconfirmation, name="account_confirm_email"),
    #end
    url(r'^registration/$',RegisterView.as_view(),name="customer_register"),
    url(r'^registration/', include('rest_auth.registration.urls')),
    url(r'^(?P<pk>[0-9]+)$',views.user_detail,name='customer-show'),
    url(r'^(?P<pk>[0-9]+)/update$',views.user_detail,name='customer-update'),
    url(r'^account/', include('allauth.urls')),
]
