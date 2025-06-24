from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string

from accounts.forms import RegisterForm, ProfileUpdateForm, RegisterFormNoCaptcha
from accounts.models import Profile
from products.models import Cart, Product, CartItem, Order, OrderItem


def send_email_confirm(request, user, new_email):
    confirm_url = request.build_absolute_uri(reverse("accounts:confirm_email"))
    confirm_url += f"?user={user.id}&email={new_email}"
    subject = "Confirm New Email"
    message = (
        f"Hello, {user.username}, you want to change your email? "
        f"To confirm this operation click on link: {confirm_url}"
    )
    send_mail(
        subject,
        message,
        from_email="noreply@gmail.com",
        recipient_list=[f"{new_email}"],
        fail_silently=False,
    )
    messages.info(request, "Confirmation Email Sent!")


def send_order_confirmation_email(order: Order):
    subject = f"Order Confirmation for Order № {Order.id}"
    context = {"order": order}
    text_content = render_to_string(
        "catalog/templates/email/order_confirmation_email.txt", context
    )
    to_email = order.contact_email
    try:
        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [to_email, settings.ADMIN_EMAIL],
        )
    except Exception as e:
        print(f"Error sending mail: {e}")
