from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('person', views.PersonView)
router.register('union', views.UnionView)
router.register('family', views.FamilyView)

urlpatterns = [
    path('', include(router.urls))
]
