from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import CategoryView

router = routers.DefaultRouter()
router.register('categories', CategoryView)

urlpatterns = [
    path('', include(router.urls))
]