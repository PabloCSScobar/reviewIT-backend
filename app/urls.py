from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('categories', CategoryView)
router.register('answers', AnswerView)
router.register('posts', PostView, basename="post")

urlpatterns = [
    path('', include(router.urls))
]
