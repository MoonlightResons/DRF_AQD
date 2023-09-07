from django.urls import path
from .views import (
    ProductCreateAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
    BasketAddProductAPIView,
    BasketDetailAPIView,
    BasketItemDeleteAPIView,
    CommentCreateAPIView,
    CommentListAPIView,
    ProductFilterAPIView,
    CommentUpdateAPIView,
    CommentDeleteAPIView
)


urlpatterns = [
    path('create/', ProductCreateAPIView.as_view(), name='products-created'),
    path('list/', ProductListAPIView.as_view(), name='products-list'),
    path('filters/', ProductFilterAPIView.as_view(), name='product-filters'),
    path('<int:id>/', ProductDetailAPIView.as_view(), name='products-detail'),
    path('update/<int:id>/', ProductUpdateAPIView.as_view(), name='products-update'),
    path('<int:id>/delete/', ProductDeleteAPIView.as_view(), name='products-delete'),
    path('<int:id>/basket/add-products/', BasketAddProductAPIView.as_view(), name='basket-add'),
    path('<int:id>/basket-info/', BasketDetailAPIView.as_view(), name='basket-detail'),
    path('<int:item_id>/basket/item/delete/', BasketItemDeleteAPIView.as_view(), name='basket-item-delete'),
    path('<int:id>/comment-create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('<int:product_id>/comment-list/', CommentListAPIView.as_view(), name='comment-list'),
    path('<int:id>/comment/delete/', CommentDeleteAPIView.as_view(), name='comment-delete'),
    path('<int:id>/comment/update/', CommentUpdateAPIView.as_view(), name='comment-update'),
]
