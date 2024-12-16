from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import UserProfileAPIView
from allauth.account.views import confirm_email

urlpatterns = [
    path("admin/", admin.site.urls),

    # API endpoints
    path('api/cart/', include('cart.urls')),
    path('api/category/', include('category.urls')),
    path('api/flower/', include('flower.urls')),
    path('api/order/', include('order.urls')),

    # REST framework and authentication
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/account-confirm-email/<str:key>/", confirm_email, name="confirm_email"),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/", include("django.contrib.auth.urls")),

    # User profile endpoint
    path('api/user-profile/', UserProfileAPIView.as_view(), name='user-profile'),

    # Password reset views
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
