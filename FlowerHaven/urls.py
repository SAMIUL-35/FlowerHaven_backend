from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from allauth.account.views import confirm_email

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/account-confirm-email/<str:key>/", confirm_email, name="confirm_email"),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("api/auth/password/reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("api/auth/password/reset/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("api/auth/password/reset/complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
