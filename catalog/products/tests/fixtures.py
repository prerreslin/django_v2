import pytest

from products.models import Category, Product, Order, OrderItem


@pytest.fixture
def product():
    category = Category.objects.create(name="test-category")
    return Product.objects.create(
        name="test-product",
        category=category,
        nomenclature="test-nomenclature",
        price=100,
    )


@pytest.fixture
def product_discount():
    category = Category.objects.create(name="test-category_2")

    return Product.objects.create(
        name="test_product",
        category=category,
        nomenclature="test-nomenclature_2",
        price=100,
        discount=10,
    )


@pytest.fixture
def order(user, product, product_discount):

    order_ = Order.objects.create(
        contact_name="test_name",
        contact_email="example@example.com",
        contact_phone="+380663831118",
        address="5 Avenue",
    )

    OrderItem.objects.create(order=order_, product=product_discount, price=100)

    OrderItem.objects.create(order=order_, product=product_discount, price=90, amount=3)

    return order_


@pytest.fixture()
def category():
    return Category.objects.create(name="Category")
