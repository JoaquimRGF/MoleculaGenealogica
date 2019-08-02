from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pessoa', views.PessoaView)
router.register('uniao', views.UniaoView)
router.register('familia', views.FamiliaView)

urlpatterns = [
    path('', include(router.urls)),
    path('pessoa/<int:pk>/spouses', views.spouses, name = "spouses")
]
