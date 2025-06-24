import pytest
# from pytest_check import check

from products.serializers.product_serializers import ProductSerializer
from products.serializers.order_serializers import OrderSerializer
from .fixtures import category, product_discount, product, order


@pytest.mark.django_db
def test_product_serializer_valid(category):
    data = {
        "name": "test_name",
        "description": "test_description",
        "stock": 3,
        "price": 100,
        "available": True,
        "category": category.id,
        "nomenclature": "test_nomenclature",
        "rating": 2,
        "discount": 10,
        "attributes": {},
    }

    serializer = ProductSerializer(data=data)

    assert serializer.is_valid()


@pytest.mark.django_db
def test_product_serializer_invalid(category):
    data = {
        "name": "*" * 101,
        "description": {},
        "stock": -3,
        "price": -100,
        "available": 2,
        "nomenclature": "*" * 101,
        "rating": "*",
        "discount": -10,
        "attributes": "*",
    }

    serializer = ProductSerializer(data=data)

    assert not serializer.is_valid()
    print(serializer.data.get("stock"))
    assert serializer.errors
    # assert (
    #     "Ensure this field has no more than 100 characters."
    #     in serializer.errors["name"]
    # )
    # assert "Must be a valid boolean." in serializer.errors["available"]
    # assert (
    #     "Ensure this field has no more than 50 characters."
    #     in serializer.errors["nomenclature"]
    # )
    # assert "A valid number is required." in serializer.errors["rating"]
    for field in data.keys():
        assert field in serializer.errors
    print(dict(serializer.errors))


# @pytest.mark.django_db
# def test_product_serializer_read_only(category):

#     data = {
#         "name": "test_name",
#         "description": "test_description",
#         "stock": 3,
#         "price": 100,
#         "available": True,
#         "category": category,
#         "nomenclature": "test_nomenclature",
#         "rating": 2,
#         "discount": 10,
#         "attributes": {},
#     }

#     serializer = ProductSerializer(data=data)
#     assert serializer.is_valid()
#     assert "category" not in serializer.data.keys()


@pytest.mark.django_db
def test_product_serializer_method_field(product_discount):
    serializer = ProductSerializer(product_discount)
    assert serializer.data["discount_price"] == product_discount.discount_price
    assert serializer.data["discount_price"] == 90


@pytest.mark.django_db
def test_order_serializer_read_only(user, order):
    data = {
        "user": user.id,
        "contact_name": "test_name",
        "contact_email": "example.example@gmail.com",
        "contact_phone": "+380663831118",
        "address": "5 Avenue",
    }

    serializer = OrderSerializer(data=data)
    assert serializer.is_valid()
    assert "items" not in serializer.validated_data
    serializer = OrderSerializer(order)
    assert "items" in serializer.data


@pytest.mark.django_db
def test_order_serializer_items(order):
    serializer = OrderSerializer(order)
    items = serializer.data["items"]

    assert len(items) == 2
