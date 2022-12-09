from django.urls import path, include
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from post.views import TestView, PostFormClassView, HomeTemplateView, PostFormView, PostCreateView, PostUpdateForm, \
    PostDeleteView, PostListView, PostDetailsView, PostLikeView, CommentView

app_name = 'post'

urlpatterns = [

    path('test/', TestView, name='test'),
    # Vanilla View
    # path('post/', PostFormClassView.as_view(), name='post-form'),

    # TemplateView
    # path('home/', HomeTemplateView.as_view(), name='home'),

    # FormView
    # path('post/', PostView.as_view(), name='post-form'),

    # CreateView
    path('add/', PostCreateView.as_view(), name='add'),

    # UpdateView
    path('update/<int:id>/', PostUpdateForm.as_view(), name='update'),

    # DeleteView
    path('delete/<int:id>/', PostDeleteView.as_view(), name='delete'),

    # ListView
    path('list/', PostListView.as_view(), name='list'),

    # DetailView
    path('details/<int:id>/', PostDetailsView.as_view(), name='details'),

    # like/comment/share
    path('like-dislike/<int:pk>/', PostLikeView, name='like_dislike'),
    path('comment/', CommentView.as_view(), name='comment'),


    # ADMIN URL
    # path('admin/', include('post.admin_urls', namespace="admin")),
]
