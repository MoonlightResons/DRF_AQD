from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField('email address', unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_Seller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


class Seller(MyUser):
    name = models.CharField(max_length=255, null=False, blank=False)
    second_name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)


class Customer(MyUser):
    name = models.CharField(max_length=255, null=False, blank=False)
    second_name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=255, null=False, blank=False)
    card_number = models.CharField(max_length=255, null=True, blank=True)
    post_code = models.CharField(max_length=255, null=True, blank=True)


class SellerRequest(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f'Request from {self.seller.name} at {self.timestamp}'
