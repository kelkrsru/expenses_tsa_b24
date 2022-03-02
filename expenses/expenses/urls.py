from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('mainpage.urls', namespace='mainpage')),
    path('card/', include('dealcard.urls', namespace='dealcard')),
    path('admin/', admin.site.urls),
    path('reports/', include('reports.urls', namespace='reports')),
]
