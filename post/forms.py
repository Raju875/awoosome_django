from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Posts, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ('is_active', 'user', 'likes', 'dislikes', 'views', 'created_by', 'updated_by')


    def form_note(self):
        pass
        # print('Hi! This is post form calss. Have a good day.')
        
    # don't work unless use "form_class=Post" in vuews.py
    def clean(self):
        # print('form clean')
        super(PostForm, self).clean()

        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')

        if name and name.lower() == 'admin':
            raise ValidationError({'name': _('Reserved name!')})
        if email and email == 'admin@gmail.com':
            raise ValidationError({'email': _('Reserved email address!.')})

        return self.cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['content', 'parent']

        labels = {
            'content': _(''),
        }

        widgets = {
            'content': forms.TextInput(),
        }
