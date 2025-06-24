import pytest

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import Profile
from products.models import Cart, Product, Category, CartItem, Order, OrderItem

from .fixtures import product, product_discount, order


@pytest.mark.django_db
def test_product_model():
    category = Category.objects.create(name="test_category")
    product = Product.objects.create(
        name="test_product",
        category=category,
        nomenclature="test_nomenclature",
        price=100,
        discount=10,
    )

    assert product.discount_price == 90
    assert product.category.name == "test_category"


@pytest.mark.django_db
def test_cart_model_one_product(user, product):
    cart_item = CartItem.objects.create(cart=user.cart, product=product)
    assert cart_item.item_total == product.price
    assert user.cart.total == product.price


@pytest.mark.django_db
def test_cart_model_multiple_products(user, product):
    cart_item = CartItem.objects.create(cart=user.cart, product=product, amount=10)
    assert cart_item.item_total == product.price * 10
    assert user.cart.total == product.price * 10


@pytest.mark.django_db
def test_cart_model_discount_product(user, product_discount):
    cart_item = CartItem.objects.create(cart=user.cart, product=product_discount)
    assert cart_item.item_total == 90
    assert user.cart.total == 90


@pytest.mark.django_db
def test_cart_model_different_products(user, product_discount, product):

    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product_discount,
    )

    cart_item_2 = CartItem.objects.create(
        cart=user.cart,
        product=product,
    )

    assert user.cart.total == 190


@pytest.mark.django_db
def test_order_model_one_item(order, product):
    order_item = OrderItem.objects.create(
        order=order, product=product, price=product.discount_price
    )

    assert order_item.amount == 1
    assert order_item.item_total == product.price


@pytest.mark.django_db
def test_order_model_multiple_items(order, product):
    order_item = OrderItem.objects.create(
        order=order, product=product, amount=10, price=product.discount_price
    )

    assert order_item.amount == 10
    assert order_item.item_total == product.price * 10


@pytest.mark.django_db
def test_order_model_discount_item(order, product_discount):
    order_item = OrderItem.objects.create(
        order=order, product=product_discount, price=product_discount.price
    )

    assert order_item.item_total == 90


@pytest.mark.django_db
def test_order_model_different_items(order, product_discount, product):

    order_item_1 = OrderItem.objects.create(
        order=order, product=product, price=product.discount_price
    )

    order_item_2 = OrderItem.objects.create(
        order=order, product=product_discount, price=product_discount.price
    )

    assert order_item_1.item_total + order_item_2.item_total == 190
