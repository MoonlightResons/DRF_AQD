from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status
from .serializer import SellerSerializer, CustomerSerializer, MyTokenObtainPairSerializer, CustomerProfileSerializer, SellerProfileSerializer
from apps.products.serializer import ProductSerializer
from .models import Seller, Customer
from .permisions import AnnonPermission
from apps.products.models import Product, Basket


class LoginView(TokenObtainPairView):
    permission_classes = (AnnonPermission,)
    serializer_class = MyTokenObtainPairSerializer


class SellerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

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


class CustomerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

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
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerListAPIView(ListAPIView):
    queryset = Seller.objects.all()
    permissions_classes = [permissions.AllowAny]
    serializer_class = SellerSerializer


class CustomerListAPIView(ListAPIView):
    queryset = Customer.objects.all()
    permissions_classes = [permissions.AllowAny]
    serializer_class = CustomerSerializer


class CustomerProfileAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        customer = Customer.objects.get(id=id)
        serializer = CustomerProfileSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerProfileAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        try:
            seller = Seller.objects.get(id=id)
            products = Product.objects.filter(seller=seller)

            seller_serializer = SellerProfileSerializer(seller)
            products_serializer = ProductSerializer(products, many=True)

            seller_data = {
                "seller_profile": seller_serializer.data,
                "products": products_serializer.data
            }

            return Response(seller_data, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response("Seller does not exist.", status=status.HTTP_404_NOT_FOUND)


class CustomerUpdateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

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


class SellerUpdateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

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


class CustomerDeleteAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellerDeleteAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id):
        try:
            seller = Seller.objects.get(id=id)
        except Seller.DoesNotExist:
            return Response({"detail": "seller not found"}, status=status.HTTP_404_NOT_FOUND)

        seller_data = {
            "id": seller.id,
            "name": seller.name,  # Замените на соответствующие поля из модели Seller
            "email": seller.email,
            # Добавьте другие поля, которые вам необходимы
        }

        seller.delete()
        return Response({"detail": "seller deleted", "seller_data": seller_data}, status=status.HTTP_200_OK)
