from rest_framework import serializers
from .models import Product, BasketItem, Comment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = BasketItem
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    comment = ProductSerializer

    class Meta:
        model = Comment
        fields = "__all__"
