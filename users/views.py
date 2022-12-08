from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import login

from .forms import UserCreateForm, CustomLoginForm, UserEditForm
from .models import CustomUser


class LoginView(LoginView):
    form_class = CustomLoginForm
    # success_url = reverse_lazy('session_cookie_cache:list')
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        print('custom login!')
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('home')
    template_name = "users/signup.html"


class ProfileView(CreateView):
    form_class = UserEditForm
    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        obj = CustomUser.objects.get(email=request.user.email)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
        return render(request, self.template_name, {'form': form})


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/change_password/password_change_form.html"
    title = _("Password change")


class PasswordChangeDoneView(PasswordResetDoneView):
    template_name = "users/change_password/password_change_done.html"
    title = _("Password reset sent")


class PasswordResetView(PasswordResetView):
    email_template_name = "users/reset_password/password_reset_email.html"
    form_class = PasswordResetForm
    subject_template_name = "users/reset_password/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "users/reset_password/password_reset_form.html"
    title = _("Password reset")


class PasswordResetDone(PasswordResetDoneView):
    template_name = "users/reset_password/password_reset_done.html"
    title = _("Password reset sent")


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = SetPasswordForm
    post_reset_login = False
    reset_url_token = "set-password"
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "users/reset_password/password_reset_confirm.html"
    title = _("Enter new password")


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "users/reset_password/password_reset_complete.html"
    title = _("Password reset complete")
