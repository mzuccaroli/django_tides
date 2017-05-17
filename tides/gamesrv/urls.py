from django.conf.urls import url, include
from rest_framework import routers
from . import views

app_name = 'games'

router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'cards', views.CardViewSet)
router.register(r'drafts', views.DraftViewSet)
router.register(r'seeds', views.SeedViewSet)
router.register(r'hands', views.HandViewSet)
router.register(r'invitations', views.InvitationViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls))
]
