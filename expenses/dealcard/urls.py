from django.urls import path, re_path
from . import views

app_name = 'dealcard'

urlpatterns = [
    path('', views.card, name='card'),
    path('expense/add/', views.add_expense, name='add_expense'),
    path('expense/<int:expense_id>/edit/', views.edit_expense,
         name='edit_expense'),
    path('expense/<int:expense_id>/delete/', views.delete_expense,
         name='delete_expense'),
]
