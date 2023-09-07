from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status

from products.views import get_object
from users.serializer import SellerSerializer, CustomerSerializer, MyTokenObtainPairSerializer, CustomerProfileSerializer, SellerProfileSerializer
from products.serializer import ProductSerializer, CommentSerializer, BasketItemSerializer
from users.models import Seller, Customer, MyUser
from users.permisions import AnnonPermission
from products.models import Product, Basket, BasketItem, Comment
from adminka.models import Admin
from adminka.permisions import IsAdminPermission
from adminka.serializer import AdminSerializer, UserSerializer
from django.db.models import Q


class AdminLoginView(TokenObtainPairView):
    permission_classes = (AnnonPermission,)
    serializer_class = MyTokenObtainPairSerializer


class AdminUserCreateView(APIView):
    permissions = [permissions.AllowAny]

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = Admin.objects.create(
                email=request.data['email'],
                is_superuser=True
            )
            admin.set_password(request.data['password'])
            admin.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSellerRegisterView(APIView):
    permission_classes = [IsAdminPermission]

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            seller = Seller.objects.create(
                email=request.data['email'],
                is_Seller=True,
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                description=request.data['description']
            )
            seller.set_password(request.data['password'])
            seller.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCustomerRegisterView(APIView):
    permission_classes = [IsAdminPermission]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = Customer.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                card_number=request.data['card_number'],
                post_code=request.data['post_code']
            )
            customer.set_password(request.data['password'])
            customer.save()
            Basket.objects.create(customer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserListAPIView(ListAPIView):
    permission_classes = [IsAdminPermission]
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class AdminCustomerUpdateAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def put(self, request, id):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerProfileSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSellerUpdateAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def put(self, request, id):
        try:
            seller = Seller.objects.get(id=id)
        except Seller.DoesNotExist:
            return Response({"detail": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SellerProfileSerializer(seller, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCustomerDeleteAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def delete(self, request, id):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminSellerDeleteAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def delete(self, request, id):
        try:
            seller = Seller.objects.get(id=id)
        except Seller.DoesNotExist:
            return Response({"detail": "seller not found"}, status=status.HTTP_404_NOT_FOUND)

        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminProductCreateAPIView(APIView):
    permissions_classes = [IsAdminPermission]

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


class AdminProductListAPIView(ListAPIView):
    permissions_classes = [IsAdminPermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AdminProductUpdateAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def put(self, request, id):
        product = get_object(id, Product)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminProductDeleteAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def delete(self, request, id):
        product = get_object(id, Product)
        product.delete()
        return Response(status=status.HTTP_200_OK)


class AdminBasketDetailAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def get(self, request, id):
        try:
            basket = Basket.objects.get(customer=id)
            basket_items = basket.items.all()
            serializer = BasketItemSerializer(basket_items, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Basket.DoesNotExist:
            return Response("Basket does not exist.", status=status.HTTP_404_NOT_FOUND)


class AdminBasketAddProductAPIView(APIView):
    permission_classes = [IsAdminPermission]

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


class AdminBasketItemDeleteAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, item_id):
        basket_item = get_object_or_404(BasketItem, id=item_id)
        basket_item.delete()
        return Response({'message': 'Предмет корзины успешно удален'}, status=status.HTTP_204_NO_CONTENT)


class AdminCommentCreateAPIView(APIView):
    permission_classes = [IsAdminPermission]

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


class AdminCommentListAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            comments = product.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response("Product does not exist.", status=status.HTTP_404_NOT_FOUND)


class AdminCommentDeleteAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminCommentUpdateAPIView(APIView):
    permission_classes = [IsAdminPermission]

    def put(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSellerAnalytics(APIView):
    def get(self, request, seller_id):
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({'message': 'Seller not found'}, status=404)

        product_count = Product.objects.filter(seller=seller).count()
        get_request_count = seller.sellerrequest_set.count()  # Подсчет количества GET-запросов к продавцу

        return Response({'product_count': product_count, 'get_request_count': get_request_count})
