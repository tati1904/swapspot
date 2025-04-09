from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('listings.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ Enables login/logout
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('listings.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ includes login/logout
]
