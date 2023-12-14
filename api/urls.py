from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

app_name='api'
urlpatterns = [
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name='login_refresh'),
    path('login-user', views.loginUser, name='login_user'),
    path('get-user-details', views.getUserDetails, name='get_user_details'),
    path('logout-user', views.logoutUser, name='logout_user'),

    path('vendors/', views.vendorListCreate, name='vendor-list-create'),
    path('vendors/<int:pk>/', views.vendorRetrieveUpdateDelete, name='vendor-retrieve-update-delete'),
    path('purchase_orders/', views.purchaseOrderListCreate, name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', views.purchaseOrderRetrieveUpdateDelete, name='purchase-order-retrieve-update-delete'),
    # path('vendors/<int:vendor_id>/performance/', views.VendorPerformanceView.as_view(), name='vendor-performance'),
]