from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import login
from django.conf import settings
from django.shortcuts import get_object_or_404

from calyvim.models import WorkspaceMembership, Workspace, Team, WorkspaceInvite, User
from calyvim.serializers import WorkspaceSerializer, ProfileSerializer, TeamSerializer
from calyvim.mixins import PermissionCheckMixin, WorkspacePermissionMixin


class WorkspaceCreateView(LoginRequiredMixin, View):
    def get(self, request):
        available_domain = None
        if not request.user.is_generic_email:
            email_domain = request.user.email.split("@")[-1]
            available_workspace_queryset = Workspace.objects.filter(
                auto_assign_domain=email_domain
            )
            if not available_workspace_queryset.exists():
                available_domain = email_domain

        context = {
            "props": {
                "base_url": settings.BASE_URL,
                "available_domain": available_domain,
            }
        }
        return render(request, "workspaces/create.html", context)


class WorkspaceIndexView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_verified:
            # Redirect them to email verification page
            return redirect("accounts-verify")

        if (
            request.user.current_workspace
            and request.user.current_workspace.deleted_at == None
        ):
            return redirect(
                "workspace-inbox",
                workspace_slug=request.user.current_workspace.slug,
            )

        workspace = request.user.workspaces.first()
        if not workspace:
            return redirect("workspace-create")

        return redirect("workspace-inbox", workspace_slug=workspace.slug)


class WorkspaceInboxView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        # Update current workspace
        if (
            not request.user.current_workspace
            or request.user.current_workspace != workspace
        ):
            request.user.current_workspace = workspace
            request.user.save(update_fields=["current_workspace"])

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "membership_role": workspace_membership.role,
                "current_user": ProfileSerializer(request.user).data,
            }
        }
        return render(request, "workspaces/inbox.html", context)


class WorkspaceBoardsView(LoginRequiredMixin, PermissionCheckMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = self.check_and_get_workpace_permssion(
            workspace, request.user
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "current_user": ProfileSerializer(request.user).data,
                "membership_role": workspace_membership.role,
            }
        }
        return render(request, "workspaces/boards.html", context)


class WorkspaceNewslinesView(LoginRequiredMixin, PermissionCheckMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = self.check_and_get_workpace_permssion(
            workspace, request.user
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "current_user": ProfileSerializer(request.user).data,
                "membership_role": workspace_membership.role,
            }
        }
        return render(request, "workspaces/newslines.html", context)


class WorkspaceMembersView(LoginRequiredMixin, WorkspacePermissionMixin, View):
    def get(self, request, workspace_slug):
        workspace = get_object_or_404(Workspace, slug=workspace_slug)

        if not self.has_valid_membership(workspace, request.user):
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "has_edit_permission": self.has_valid_permission(
                    workspace, request.user, ["admin", "maintainer"]
                ),
            }
        }
        return render(request, "workspaces/settings/members.html", context)


class WorkspaceTeamsView(LoginRequiredMixin, WorkspacePermissionMixin, View):
    def get(self, request, workspace_slug):
        workspace = get_object_or_404(Workspace, slug=workspace_slug)

        if not self.has_valid_membership(workspace, request.user):
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "has_edit_permission": self.has_valid_permission(
                    workspace, request.user, ["admin", "maintainer"]
                ),
            }
        }
        return render(request, "workspaces/settings/teams/index.html", context)


class WorkspaceTeamsEditView(LoginRequiredMixin, WorkspacePermissionMixin, View):
    def get(self, request, workspace_slug, team_id):
        workspace = get_object_or_404(Workspace, slug=workspace_slug)

        if not self.has_valid_membership(workspace, request.user):
            raise Http404

        if not self.has_valid_permission(
            workspace=workspace,
            user=request.user,
            allowed_roles=["admin", "maintainer"],
        ):
            raise Http404

        team = get_object_or_404(Team, workspace=workspace, id=team_id)

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "team": TeamSerializer(team).data,
            }
        }
        return render(request, "workspaces/settings/teams/edit.html", context)


class WorkspaceSettingsGeneralView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "current_user": ProfileSerializer(request.user).data,
                "membership_role": workspace_membership.role,
            }
        }
        return render(request, "workspaces/settings/general.html", context)


class WorkspaceSettingsBillingView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "current_user": ProfileSerializer(request.user).data,
                "membership_role": workspace_membership.role,
            }
        }
        return render(request, "workspaces/settings/billing.html", context)


class WorkspaceMemberConfirmationView(View):
    def get(self, request, *args, **kwargs):
        invite = WorkspaceInvite.objects.filter(
            workspace__slug=kwargs.get("workspace_slug"),
            invitation_id=kwargs.get("invitation_id"),
            confirmed_at__isnull=True,
        ).first()

        if not invite:
            raise Http404

        # Check for existing user with the invite email
        user = User.objects.filter(email=invite.email).first()
        if not user:
            # Redirect to register page along with invitation ID
            return redirect(
                reverse("accounts-register") + f"?invitation_id={invite.invitation_id}"
            )

        try:
            if not user.is_verified:
                user.verify()

            with transaction.atomic():
                WorkspaceMembership.objects.create(
                    user=user, workspace=invite.workspace
                )
                invite.confirm_invitation()

        except Exception as e:
            print(e)

        # login(request, user)
        # return redirect("workspace-inbox", workspace_slug=invite.workspace.slug)
        # Generate access token and redirect to login page
        redirect_url = reverse("accounts-login") + f"?session={user.session}"
        return redirect(redirect_url)


class WorkspaceLeaveView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user
        ).first()
        if not workspace_membership:
            raise Http404

        if workspace.created_by == request.user:
            # Don't allow to leave org to workspace owners
            messages.warning(request, "Workspace owners can't leave workspace.")
            return redirect("workspace-inbox", workspace_slug=workspace.slug)

        workspace_membership.delete()
        return redirect("workspace-index")


class WorkspaceDeleteView(LoginRequiredMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = WorkspaceMembership.objects.filter(
            workspace=workspace, user=request.user, role=WorkspaceMembership.Role.ADMIN
        ).first()
        if not workspace_membership:
            raise Http404

        # Mark the workspace as deleted.
        workspace.soft_delete()

        # Remove current workspace from all users
        User.objects.filter(current_workspace=workspace).update(current_workspace=None)
        return redirect("workspace-index")


class WorkspaceTodosView(LoginRequiredMixin, PermissionCheckMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = self.check_and_get_workpace_permssion(
            workspace, request.user
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "current_user": ProfileSerializer(request.user).data,
                "membership_role": workspace_membership.role,
            }
        }
        return render(request, "workspaces/todos.html", context)


class WorkspaceDocumentsView(LoginRequiredMixin, PermissionCheckMixin, View):
    def get(self, request, workspace_slug):
        workspace = Workspace.objects.filter(slug=workspace_slug).first()
        if not workspace:
            raise Http404

        workspace_membership = self.check_and_get_workpace_permssion(
            workspace, request.user
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(workspace).data,
                "current_user": ProfileSerializer(request.user).data,
                "membership_role": workspace_membership.role,
            }
        }
        return render(request, "workspaces/documents.html", context)
