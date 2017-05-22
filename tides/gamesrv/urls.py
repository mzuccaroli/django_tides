from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'cards', views.CardViewSet)
router.register(r'drafts', views.DraftViewSet)
router.register(r'seeds', views.SeedViewSet)
router.register(r'hands', views.HandViewSet)
router.register(r'invitations', views.InvitationViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.AllGamesList.as_view(), name='allgames'),
    url(r'^invite$', views.new_invitation, name='tides_invite'),
    url(r'^invitation/(?P<pk>\d+)/$', views.accept_invitation, name='tides_accept_invitation'),

]
