import json

from django.contrib.auth.models import User
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from ..models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "available",
            "category",
            "nomenclature",
            "created_at",
            "rating",
            "discount",
            "attributes",
            "discount_price",
        ]

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_discount_price(self, obj):
        if isinstance(obj, dict):
            return obj.get("discount_price")
        return getattr(obj, "discount_price", None)

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("The price should be higher than 0")
        else:
            return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("The stock should be higher than 0")
        else:
            return value

    def validate_description(self, value):
        if isinstance(value, str):
            return value
        else:
            raise serializers.ValidationError("Description must be text")

    def validate_discount(self, value):
        if value < 0:
            raise serializers.ValidationError("The discount should be higher than 0")
        else:
            return value

    # def validate_category(self, value):
    #     if not (isinstance(value, int)) or not (isinstance(value, Category)):
    #         raise serializers.ValidationError(
    #             "Category must be int or Category instance"
    #         )
    #     else:
    #         return value

    def validate_attributes(self, value):
        if not value:
            return value
        try:
            return json.loads(value)
        except Exception:
            raise serializers.ValidationError(f"Attributes must be a valid json")
