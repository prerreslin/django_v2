from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("products.urls", namespace="products")),
    path("", include("accounts.urls", namespace="accounts")),
    path("captcha/", include("captcha.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        # path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("api/refresh/", TokenObtainPairView.as_view(), name="token_refresh"),
    ]
