from django.conf.urls import url
from admin_user import views

urlpatterns = [
    url(r'^users$',views.index,name='users'),
    # url(r'^users/create$',views.store,name='user-create'),
    url(r'^users/(?P<pk>[0-9]+)$',views.user_detail,name='user-show'),
    url(r'^users/(?P<pk>[0-9]+)/update$',views.user_detail,name='user-update'),
    url(r'^users/(?P<pk>[0-9]+)/delete$',views.user_detail,name='user-delete')
]
