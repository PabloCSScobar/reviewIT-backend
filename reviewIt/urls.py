from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('auth/', views.obtain_auth_token)
]
