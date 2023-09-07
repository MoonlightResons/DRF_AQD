from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Customer, Seller
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        token['is_Seller'] = user.is_Seller
        return token


class SellerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Seller.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = Seller
        fields = [
            'id',
            'email',
            'name',
            'second_name',
            'phone_number',
            'description',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didnt match!'}
            )
        return attrs


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Customer.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = Customer
        fields = [
            'id',
            'email',
            'name',
            'second_name',
            'phone_number',
            'card_number',
            'post_code',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didnt match!'}
            )
        return attrs


class CustomerProfileSerializer(serializers.ModelSerializer):
    customer = Customer

    class Meta:
        model = Customer
        exclude = ['password', 'is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions']


class SellerProfileSerializer(serializers.ModelSerializer):
    seller = Seller

    class Meta:
        model = Seller
        exclude = ['password', 'is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions']


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        exclude = ['password', 'is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions']
