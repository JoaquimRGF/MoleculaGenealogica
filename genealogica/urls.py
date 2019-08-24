from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('person', views.PersonView)
router.register('family', views.FamilyView)
router.register('links', views.LinksView)


urlpatterns = [
    path('', include(router.urls))
]
