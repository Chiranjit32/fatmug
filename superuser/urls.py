from django.contrib import admin
from django.urls import path
from . import views

app_name = 'superuser'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('vendor-list', views.vendorList, name='vendorList'),
    path('vendor-add', views.vendorAdd, name='vendorAdd'),
    path('vendor-edit/<int:id>', views.vendorEdit, name='vendorEdit'),

    path('purchase-order-list', views.purchaseOrderList, name='purchaseOrderList'),
    path('purchase-order-add', views.purchaseOrderAdd, name='purchaseOrderAdd'),
    path('purchase-order-edit/<int:id>', views.purchaseOrderEdit, name='purchaseOrderEdit'),
    path('purchase-order-view/<int:id>', views.purchaseOrderView, name='purchaseOrderView'),
]
