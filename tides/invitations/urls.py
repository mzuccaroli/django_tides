from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'invitations', views.InvitationViewSet)

urlpatterns = [
    url(r'^$', views.AllInvitationsList.as_view(), name='allinvitations'),
    url(r'^invite$', views.new_invitation, name='tides_invite'),
    url(r'^/(?P<pk>\d+)/$', views.accept_invitation, name='tides_accept_invitation'),

]
