from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('finance/', views.report_finance, name='report_finance'),
    path('buh/', views.report_buh, name='report_buh')
]