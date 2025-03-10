import random
import jwt
from django.db import models, transaction
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.apps import apps

from calyvim.models.base import UUIDTimestampModel


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, first_name, password):
        user = self.model(
            username=username, email=self.normalize_email(email), first_name=first_name
        )
        user.set_password(password)
        user.is_admin = True
        user.verified_at = timezone.now()
        user.save(using=self._db)

        return user


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(verified_at__isnull=False)
            .filter(restricted_at__isnull=True)
        )


class User(UUIDTimestampModel, AbstractBaseUser):
    current_workspace = models.ForeignKey(
        "Workspace", on_delete=models.SET_NULL, null=True, blank=True
    )
    username = models.CharField(max_length=124, unique=True, blank=True)
    email = models.CharField(max_length=124, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    display_name = models.CharField(max_length=124, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="user-avatars/")
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    is_password_expired = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_generic_email = models.BooleanField(default=True)

    restricted_at = models.DateTimeField(blank=True, null=True)

    verification_id = models.CharField(max_length=64, blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    verification_sent_at = models.DateTimeField(blank=True, null=True)

    password_reset_id = models.CharField(max_length=64, blank=True, null=True)
    password_reset_sent_at = models.DateTimeField(blank=True, null=True)

    # OAuth Fields
    google_id = models.CharField(max_length=64, blank=True, null=True)
    github_id = models.CharField(blank=True, null=True, max_length=64)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name"]
    EMAIL_FIELD = "email"

    class Meta:
        db_table = "users"

    objects = UserManager()
    active_objects = ActiveUserManager()

    def __str__(self) -> str:
        return f"{self.username} <{self.email}>"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.display_name:
                self.display_name = f"{self.first_name} {self.last_name}"

            if not self.username:
                self.username = slugify(self.first_name) + str(random.randint(100, 999))

            # Determine if the email domain is generic
            email_domain = self.email.split("@")[-1].lower()
            self.is_generic_email = email_domain in self.public_domains()

            if not self.verified_at:
                self.verification_id = get_random_string(18)
        return super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def is_verified(self):
        return self.verified_at is not None

    def verify(self):
        self.verified_at = timezone.now()
        self.verification_id = None
        self.save(update_fields=["verified_at", "verification_id"])

    def verify_confirm(self):
        self.verified_at = timezone.now()
        self.verification_id = None
        self.save(update_fields=["verified_at", "verification_id"])

    @property
    def verification_link(self):
        if not self.verification_id:
            self.verification_id = get_random_string(18)
            self.save(update_fields=["verification_id"])

        return settings.BASE_URL + reverse(
            "accounts-verify-confirm", args=[self.verification_id]
        )

    @transaction.atomic
    def password_reset_confirm(self, new_password):
        self.set_password(new_password)
        self.password_reset_id = None
        self.save()

    @property
    def password_reset_link(self):
        if not self.password_reset_id:
            self.password_reset_id = get_random_string(64)
            self.password_reset_sent_at = timezone.now()
            self.save(update_fields=["password_reset_id", "password_reset_sent_at"])

        return settings.BASE_URL + reverse(
            "accounts-reset-confirm", args=[self.password_reset_id]
        )

    def public_domains(self):
        return {
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "icloud.com",
            "protonmail.com",
            "zoho.com",
            "aol.com",
            "yandex.com",
            "yandex.ru",
            "mail.com",
            "gmx.com",
            "tutanota.com",
            "fastmail.com",
            "hey.com",
            "mail.ru",
        }

    @property
    def session(self):
        return jwt.encode(
            {
                "user_id": str(self.id),
                "exp": timezone.now() + timezone.timedelta(minutes=10),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    def assign_membership_via_domain(self):
        if not self.is_generic_email:
            Workspace = apps.get_model("calyvim", "Workspace")
            WorkspaceMembership = apps.get_model("calyvim", "WorkspaceMembership")
            domain = self.email.split("@")[1]
            workspace = Workspace.objects.filter(auto_assign_domain=domain).first()
            if workspace and workspace.auto_assign_membership:
                # Check for membership
                membership = WorkspaceMembership.objects.filter(
                    user=self, workspace=workspace
                ).first()
                if not membership:
                    WorkspaceMembership.objects.create(
                        user=self,
                        workspace=workspace,
                        role=WorkspaceMembership.Role.COLLABORATOR,
                    )
