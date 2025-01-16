import uuid
import httpx
from urllib.parse import urlencode
from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404
from django.urls import reverse
from django.views import View
from django.contrib.auth import logout, login
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings

from rest_framework import serializers

from calyvim.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "display_name", "username"]


class LoginView(View):
    def get(self, request):
        next = request.GET.get("next", "/")
        session = request.GET.get("session", None)

        has_google_oauth = (
            settings.GOOGLE_OAUTH_CLIENT_ID is not None
            and settings.GOOGLE_OAUTH_CLIENT_ID is not None
        )
        has_github_oauth = (
            settings.GITHUB_OAUTH_CLIENT_ID is not None
            and settings.GITHUB_OAUTH_CLIENT_SECRET is not None
        )

        context = {
            "props": {
                "next": next,
                "session": session,
                "has_google_oauth": has_google_oauth,
                "has_github_oauth": has_github_oauth,
            }
        }
        return render(request, "accounts/login.html", context)


class RegisterView(View):
    def get(self, request):
        has_google_oauth = (
            settings.GOOGLE_OAUTH_CLIENT_ID is not None
            and settings.GOOGLE_OAUTH_CLIENT_ID is not None
        )
        has_github_oauth = (
            settings.GITHUB_OAUTH_CLIENT_ID is not None
            and settings.GITHUB_OAUTH_CLIENT_SECRET is not None
        )
        context = {
            "props": {
                "invitation_id": request.GET.get("invitation_id", None),
                "has_google_oauth": has_google_oauth,
                "has_github_oauth": has_github_oauth,
            }
        }
        return render(request, "accounts/register.html", context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts-login")


class VerifyView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_verified:
            return redirect("accounts-login")

        context = {
            "props": {
                "current_user": UserSerializer(request.user).data,
            }
        }

        return render(request, "accounts/verify.html", context)


class VerifyConfirmView(View):
    def get(self, request, verification_id):
        user = User.objects.filter(verification_id=verification_id).first()
        if not user:
            raise Http404

        user.verify_confirm()

        # Generate access token and redirect to login page
        redirect_url = reverse("accounts-login") + f"?session={user.session}"
        return redirect(redirect_url)


class ResetView(View):
    def get(self, request):
        return render(request, "accounts/reset.html")


class ResetConfirmView(View):
    def get(self, request, password_reset_id):
        user = User.objects.filter(password_reset_id=password_reset_id).first()
        if not user:
            raise Http404()

        context = {"props": {"password_reset_id": password_reset_id}}
        return render(request, "accounts/reset_confirm.html", context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/profile.html")


class SecurityView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/security.html")


class OAuthGoogleSessionView(View):
    def get(self, request):
        print(
            "REDIRECT URI",
            settings.BASE_URL + reverse("accounts-oauth-google-callback"),
        )
        scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]
        params = {
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "redirect_uri": settings.BASE_URL
            + reverse("accounts-oauth-google-callback"),
            "response_type": "code",
            "scope": " ".join(scopes),
            "access_type": "offline",
            "state": uuid.uuid4().hex,
            "include_granted_scopes": "true",
        }
        redirect_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        )
        print("REDIRECT URL", redirect_url)
        return redirect(redirect_url)


class OAuthGoogleCallbackView(View):
    def get(self, request):
        authorization_params = {
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "code": request.GET.get("code"),
            "grant_type": "authorization_code",
            "redirect_uri": settings.BASE_URL
            + reverse("accounts-oauth-google-callback"),
        }

        authorization_response = httpx.post(
            url="https://oauth2.googleapis.com/token", data=authorization_params
        )

        if authorization_response.status_code != 200:
            raise Http404("Failed to retrieve authorization token")

        userinfo_response = httpx.get(
            url="https://www.googleapis.com/oauth2/v2/userinfo",
            headers={
                "Authorization": f"Bearer {authorization_response.json()['access_token']}"
            },
        )

        if userinfo_response.status_code != 200:
            raise Http404("Failed to retrieve user info")

        user_data = userinfo_response.json()
        # Check if user exists
        user = User.objects.filter(email=user_data["email"]).first()
        if not user:
            user = User.objects.create(
                email=user_data["email"],
                first_name=user_data.get("given_name", None),
                last_name=user_data.get("family_name"),
            )
        if not user.is_verified:
            user.verify()

        if not user.google_id:
            user.google_id = str(user_data["id"])
            user.save(update_fields=["google_id"])

        # Generate access token and redirect to login page
        redirect_url = reverse("accounts-login") + f"?session={user.session}"
        return redirect(redirect_url)
