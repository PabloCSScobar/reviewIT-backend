from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken import views
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('auth/', views.obtain_auth_token),
    path('__debug__/', include(debug_toolbar.urls)),
]
