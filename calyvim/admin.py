from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html

from calyvim.models import (
    User,
    Board,
    State,
    Task,
    TaskAssignee,
    Priority,
    Workspace,
    WorkspaceMembership,
    Team,
    TeamMembership,
    WorkspaceInvite,
    TaskComment,
    TaskLabel,
    Label,
    BoardPermission,
    BoardTeamPermission,
    Newsline,
    NewslineTeamPermission,
    NewslinePermission,
    Estimate,
    Sprint,
    Document,
    TaskSnapshot,
)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "username", "is_admin"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "username", "is_admin", "login_link"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Personal info",
            {
                "fields": [
                    "username",
                    "first_name",
                    "last_name",
                    "display_name",
                    "avatar",
                ]
            },
        ),
        (
            "Permissions",
            {
                "fields": [
                    "is_admin",
                    "verified_at",
                    "verification_id",
                    "is_generic_email",
                ]
            },
        ),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

    def login_link(self, obj):
        url = reverse("accounts-login") + f"?session={obj.session}"
        return format_html('<a href="{}">Login</a>', url)

    login_link.short_description = "Login"


class WorkspaceMembershipAdmin(admin.StackedInline):
    model = WorkspaceMembership
    extra = 0


class WorkspaceInviteInlineAdmin(admin.StackedInline):
    model = WorkspaceInvite
    extra = 0


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    raw_id_fields = ["created_by"]
    inlines = [WorkspaceMembershipAdmin, WorkspaceInviteInlineAdmin]


class BoardPermissionInlineAdmin(admin.StackedInline):
    model = BoardPermission
    extra = 0


class BoardTeamPermissionInlineAdmin(admin.StackedInline):
    model = BoardTeamPermission
    extra = 0


class EstimateInlineAdmin(admin.StackedInline):
    model = Estimate
    extra = 0


class SprintInlineAdmin(admin.StackedInline):
    model = Sprint
    extra = 0


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ["name", "created_by"]
    raw_id_fields = ["created_by"]
    inlines = [
        BoardTeamPermissionInlineAdmin,
        BoardPermissionInlineAdmin,
        EstimateInlineAdmin,
        SprintInlineAdmin,
    ]


class TeamMembershipInline(admin.StackedInline):
    model = TeamMembership
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    inlines = [TeamMembershipInline]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ["name", "color"]


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


class TaskAssigneeInlineAdmin(admin.StackedInline):
    model = TaskAssignee
    extra = 1


class TaskCommentInlineAdmin(admin.StackedInline):
    model = TaskComment
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "summary", "sprint", "created_at"]
    inlines = [TaskAssigneeInlineAdmin, TaskCommentInlineAdmin]


class NewslinePermissionInline(admin.StackedInline):
    model = NewslinePermission
    extra = 0


@admin.register(Newsline)
class NewslineAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at"]
    inlines = [NewslinePermissionInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "created_at"]
    raw_id_fields = ["author"]


@admin.register(TaskSnapshot)
class TaskSnapshotAdmin(admin.ModelAdmin):
    list_display = ["task", "state", "date"]


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
