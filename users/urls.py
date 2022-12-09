from django.urls import path, include
from django.contrib.auth import views as auth_views

from users.views import SignUpView, LoginView, ProfileView, PasswordChangeView, PasswordResetView,\
    PasswordChangeDoneView, PasswordResetDone, PasswordResetConfirm, PasswordResetComplete

app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    # path("login/", auth_views.LoginView.as_view(template_name='users/login.html')),
    path("login/", LoginView.as_view(), name="login"),

    # profile
    path('profile/', ProfileView.as_view(), name='profile'),

    # change password
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),


    path("", include("django.contrib.auth.urls")),
]
