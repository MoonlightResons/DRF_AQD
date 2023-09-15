from django.urls import path
from .views import (
    CustomerRegisterView,
    SellerRegisterView,
    LoginView,
    CustomerListAPIView,
    SellerListAPIView,
    CustomerProfileAPIView,
    SellerProfileAPIView,
    CustomerUpdateAPIView,
    SellerUpdateAPIView,
    CustomerDeleteAPIView,
    SellerDeleteAPIView,
)

urlpatterns = [
    path('register/seller/', SellerRegisterView.as_view(), name='seller-register'),
    path('register/customer/', CustomerRegisterView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('seller/list/', SellerListAPIView.as_view(), name='seller-list'),
    path('customer/list/', CustomerListAPIView.as_view(), name='customer-list'),
    path('<int:id>/customer/profile/', CustomerProfileAPIView.as_view(), name='customer-profile'),
    path('<int:id>/seller/profile/', SellerProfileAPIView.as_view(), name='seller-profile'),
    path('<int:id>/customer/update/', CustomerUpdateAPIView.as_view(), name='customer-update'),
    path('<int:id>/seller/update/', SellerUpdateAPIView.as_view(), name='seller-update'),
    path('<int:id>/customer/delete/', CustomerDeleteAPIView.as_view(), name='customer-delete'),
    path('<int:id>/seller/delete/', SellerDeleteAPIView.as_view(), name='seller-delete'),
]
