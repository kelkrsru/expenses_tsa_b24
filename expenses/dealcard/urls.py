from django.urls import path, include
from . import views

app_name = 'dealcard'

urlpatterns = [
    path('', views.card, name='card'),
    path('expense/add/', views.add_expense, name='add_expense')
]