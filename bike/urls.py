from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('login/', views.logins),
    path('logout/', views.logouts),
    path('detail/<int:ID>/', views.detail),
    path('rent/<int:ID>/', views.rent),
    path('transactions/', views.transactions),
    path('transaction/<int:ID>/', views.transaction),
    path('feedback/<int:ID>/', views.feedback),
    path('finish/<int:ID>/', views.finish),
    path('charge/', views.charge),
    path('chart/', views.chart)
]