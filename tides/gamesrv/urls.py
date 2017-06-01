from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'cards', views.CardViewSet)
router.register(r'drafts', views.DraftViewSet)
router.register(r'seeds', views.SeedViewSet)
router.register(r'hands', views.HandViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.AllGamesList.as_view(), name='allgames'),
    url(r'^(?P<pk>\d+)/$', views.game_detail, name='game_detail'),
    url(r'^card/(?P<pk>\d+)/$', views.card_detail, name='card_detail')
]
