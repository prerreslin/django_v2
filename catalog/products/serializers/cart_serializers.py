from django.contrib.auth.models import User
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from .product_serializers import ProductSerializer

from ..models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    item_total = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_item_total(self, obj):
        return obj.item_total

    class Meta:
        model = CartItem
        fields = ["cart", "product", "amount", "item_total"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        else:
            return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="cart_items", many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["user", "created_at", "items", "total"]

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total(self, obj):
        return obj.total
