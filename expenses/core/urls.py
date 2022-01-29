from django.urls import path, include
from .views import index

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
]