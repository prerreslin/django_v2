from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiTypes

from ..forms import RegisterForm, ProfileUpdateForm, RegisterFormNoCaptcha, LoginForm
from ..models import Profile
from utils.email import send_email_confirm
from products.models import Cart, Product, CartItem
from utils.email import send_email_confirm
from ..serializers import ProfileSerializer, UserSerializer, RegisterFormSerializer


class AccountViewSet(ViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @extend_schema(
        request=RegisterFormSerializer,
        responses={201: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    @action(detail=False, methods=["post"])
    def register(self, request):
        form = RegisterForm(request.data)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            login(request, user)
            send_email_confirm(request, user, user.email)
            return Response({"message": "User was registered!"}, status=201)

        else:
            return Response({"errors": form.errors}, status=400)

    @action(detail=False, methods=["post"])
    def login(self, request):
        form = LoginForm(request.data)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if user:
                login(request, user)
                session_cart = request.session.get(settings.CART_SESSION_ID, default={})

                if session_cart:
                    cart = request.user.cart

                    for p_id, amount in session_cart.items():
                        product = Product.objects.get(id=p_id)
                        cart_item, created = CartItem.objects.get_or_create(
                            cart=cart, product=product
                        )
                        cart_item.amount = (
                            cart_item.amount + amount if not created else amount
                        )
                        cart_item.save()

                    session_cart.clear()

                return Response({"message": "Successful login"}, ststus=200)

            return Response({"eror": "Incorrect login or password"}, status=400)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout_view(self, request):
        logout(request)
        return Response({"message": "Successfully logout"})

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def profile_view(self, request):
        profile = request.user.profile
        data = ProfileSerializer(profile).data
        return Response({"results": data})

    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    def edit_profile(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(request.data, request.FILES, user=request.user)

        if form.is_valid():
            new_email = form.cleaned_data.get("email")
            if new_email != request.user.email:
                send_email_confirm(request, request.user, new_email)

            avatar = form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar

            profile.save()
            return Response({"results": ProfileSerializer(profile).data}, status=200)

        else:
            return Response(form.errors, status=400)

    @action(detail=False, methods=["get"])
    def confirm_email(self, request):
        user_id = request.GET.get("user")
        new_email = request.GET.get("email")

        if not user_id or not new_email:
            return Response({"error": "Invalid URL"}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.is_active and User.objects.filter(email=new_email).exists():
            return Response({"error": "this email is already used"}, status=400)

        user.email = new_email
        user.is_active = True
        user.save()
        return Response({"results": UserSerializer(user).data}, status=200)
