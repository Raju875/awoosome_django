from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from django.utils.timesince import timesince
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.urls import reverse

from utils.image import file_upload
from abstract_app.models import Common

User = get_user_model()

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name__icontains='Al')


class Posts(Common):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='post', related_query_name='pq')
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    message = models.CharField(max_length=2000)
    test_count = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=2000, blank=True, null=True)
    photo = models.ImageField(upload_to=file_upload, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='like_post')
    dislikes = models.ManyToManyField(User, related_name='dislike_post')
    views = models.ManyToManyField(User, related_name='view_post')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_post', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_post', null=True)

    obj = models.Manager()
    custom = CustomManager()

    class Meta:
        permissions = [
            ("change_post_status", "Can change the status of posts")
        ]
        ordering = ('-id', )
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.name

    def get_list_url(self):
        return reverse('post:list')

    def get_absolute_url(self):
        return reverse('post:details', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('post:update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'id': self.id})
    
    def get_like_dislike_url(self):
        return reverse('post:like_dislike', kwargs={'pk': self.id})

    def clean(self):
        name = self.name
        email = self.email
        if name.lower()=='admin':
            raise ValidationError({'name': _('Reserved name!')})
        if email=='admin@gmail.com':
            raise ValidationError({'email': _('Reserved email address!.')})

    def image_tag(self):
        if self.photo:
            return mark_safe('<img style="width: 50px; height=50px" src="%s" alt="photo">' % (self.photo.url))
        else:
            return mark_safe('<img style="width: 50px; height=50px;" src="%s" alt="default photo">' % ('/media/default/default.png'))


    @property
    def model_note(self):
        return True
        print('Hi! This is post model calss. Have a good day.')
        return "have a good day!"

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def total_views(self):
        return self.views.count()

    def get_time_diff(self):
        # Needed to convert time to a datetime object
        dummydate = datetime.date(2000, 1, 1)
        dt1 = datetime.combine(dummydate, self.t1)
        dt2 = datetime.combine(dummydate, self.t2)
        return timesince(dt1, dt2)

    # don't need if use form_valid & fomr_inavlid function in generic views
    # def save(self, *args, **kwargs):
    #     if self._state.adding == True and self.pk is None:
    #         print('save')
    #     if self._state.adding == False and self.pk:
    #         print('update')

    # def delete(self, *args, **kwargs):
    #     print('delete')


class Comment(Common):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering=['-updated_at']

    def __str__(self):
        return self.user.username + ": " + self.content[0:15]

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
