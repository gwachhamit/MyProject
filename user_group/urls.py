from django.conf.urls import url
from user_group import views
from django.urls import include

urlpatterns = [
    url(r'^$',views.index,name='group-list'),
    url(r'^create$',views.create,name='group-create'),
    url(r'^(?P<pk>[0-9]+)$',views.group_detail,name='group-show'),
    url(r'^(?P<pk>[0-9]+)/update$',views.group_update,name='group-update'),
    url(r'^(?P<pk>[0-9]+)/delete$',views.group_delete,name='group-delete'),

    url(r'^permissions$',views.listPermissions,name="permission-list"),
]
