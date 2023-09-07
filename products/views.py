from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework import permissions, status, generics
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProductSerializer, BasketItemSerializer, CommentSerializer
from .models import Product, BasketItem, Basket, Comment, Rate
from users.permisions import IsSellerPermission, IsOwnerOrReadOnly, IsOwnerOfBasket
from rest_framework.pagination import PageNumberPagination


class PaginationAPINumber(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 10


def get_object(id, table):
    try:
        return table.objects.get(id=id)
    except table.DoesNotExist:
        raise Http404


class ProductCreateAPIView(APIView):
    pagination_class = PaginationAPINumber
    permissions_classes = [IsSellerPermission]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create(
                name=request.data['name'],
                description=request.data['description'],
                price=request.data['price'],
                seller_id=request.data['seller'],
                category_id=request.data['category'],
            )
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    permissions_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer



class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        product = get_object(id, Product)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateAPIView(APIView):
    permission_classes = [IsSellerPermission, IsOwnerOrReadOnly]

    def put(self, request, id):
        product = get_object(id, Product)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsSellerPermission, IsOwnerOrReadOnly]

    def delete(self, request, id):
        product = get_object(id, Product)
        product.delete()
        return Response(status=status.HTTP_200_OK)


class BasketAddProductAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, id):
        try:
            basket = Basket.objects.get(customer=id)
        except Basket.DoesNotExist:
            # Если корзины нет, вы можете создать ее или вернуть ошибку
            return Response({'message': 'Корзина не существует'}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # Если продукта нет, вернуть ошибку
            return Response({'message': 'Продукт не существует'}, status=status.HTTP_404_NOT_FOUND)

        basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)
        serializer = BasketItemSerializer(basket_item)

        if not created:
            basket_item.quantity += 1
            basket_item.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class BasketDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        try:
            basket = Basket.objects.get(customer=id)
            basket_items = basket.items.all()
            serializer = BasketItemSerializer(basket_items, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Basket.DoesNotExist:
            return Response("Basket does not exist.", status=status.HTTP_404_NOT_FOUND)


class BasketItemDeleteAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, item_id):
        basket_item = get_object_or_404(BasketItem, id=item_id)
        basket_item.delete()
        return Response({'message': 'Предмет корзины успешно удален'}, status=status.HTTP_204_NO_CONTENT)


class CommentCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response("Product does not exist.", status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            comments = product.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response("Product does not exist.", status=status.HTTP_404_NOT_FOUND)


class CommentDeleteAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentUpdateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductFilterAPIView(APIView):
    def get(self, request):
        category = request.query_params.get('category', None)
        price = request.query_params.get('price', None)
        order = request.query_params.get('order', None)
        rating_order = request.query_params.get('rating_order', None)

        queryset = Product.objects.all()

        if category:
            queryset = queryset.filter(category__name=category)

        if price:
            queryset = queryset.filter(price__lte=price)

        if order == 'low_to_high':
            queryset = queryset.order_by('price')
        elif order == 'high_to_low':
            queryset = queryset.order_by('-price')

        if rating_order == 'low_to_high':
            queryset = queryset.order_by('rating')
        elif rating_order == 'high_to_low':
            queryset = queryset.order_by('-rating')

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
