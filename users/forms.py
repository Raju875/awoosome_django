
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from .models import CustomUser


# UserCreationForm is buit in django form to use for user signup
class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields =  ("name", "email", "username", "address", "phone")


# UserChangeForm is buit in django form to use for user profile change
class UserEditForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['last_login'].disabled = True
        self.fields['date_joined'].disabled = True

    password = None
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ("name", "email", "address", "phone", "last_login", "date_joined")


# AuthenticationForm is buit in django form to use for user login
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
