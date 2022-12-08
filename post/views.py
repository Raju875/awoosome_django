from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages, sites
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect, render
from django.middleware.csrf import CsrfViewMiddleware
from django import setup

from .forms import PostForm, CommentForm
from .models import Posts, Comment


# Test View
def TestView(request):
    """I am test view"""
    current_site = Site.objects.get_current()
    print(current_site.name)
    print(get_current_site(request))
    return HttpResponse('I am test view!')


# Vanilla View
class PostFormClassView(View):
    template_name = "post/add.html"
    form_class = PostForm
    success_url = '.'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('.')
        return render(request, self.template_name, {'form': form})


# TemplateView
class HomeTemplateView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msg'] = 'Welcome to our home page'
        return context


# FormView
class PostFormView(FormView):
    template_name = "post/add.html"
    form_class = PostForm
    success_url = reverse_lazy('post:home')

    def form_valid(self, form):
        form.save()
        form.form_note()
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        return super().form_invalid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(PostFormView, self).get_initial(**kwargs)
        initial['message'] = 'My sample message'
        return initial


# CreateView
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'post.add_posts'
    # model = Posts
    # fields = '__all__'
    form_class = PostForm
    template_name = "post/add.html"
    # success_url = reverse_lazy('post:list')

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Data stored successfully')
        return reverse_lazy('post:details', kwargs={'id': self.object.id})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.created_by = self.request.user
        post.updated_by = self.request.user
        post.is_active = True
        post.save()

        # self.model(self).model_note()
        # form.form_note()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(3)
        print('invalid')
        return super().form_invalid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(PostCreateView, self).get_initial(**kwargs)
        initial['message'] = 'My sample message'
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PostCreateView, self).get_form_kwargs(*args, **kwargs)
        # kwargs['user'] = self.request.user
        return kwargs


# UpdateView
class PostUpdateForm(PermissionRequiredMixin, UpdateView):
    permission_required = 'post.change_posts'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    template_name = "post/add.html"
    # form_class = PostForm
    model = Posts
    fields = ['name', 'email', 'phone', 'message', 'photo']
    # success_url = reverse_lazy('post:list')
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Data updated successfully')
        return reverse_lazy('post:details', kwargs={'id': self.object.id})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.is_active = True
        post.save()
        self.model(self).model_note
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        messages.success(self.request, _("Data loaded successfully"))
        return context

    # custom query
    # def get_queryset(self):
    #   queryset = super(PostUpdateForm, self).get_queryset()
    #   return queryset.filter(id=33)


# DeleteView
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'post.delete_posts'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    model = Posts
    template_name = 'post/delete.html'
    success_url = reverse_lazy('post:list')

    # custom query
    # def get_queryset(self):
    #   queryset = super(PostDeleteView, self).get_queryset()
    #   return queryset.filter(id=33)


# ListView
class PostListView(PermissionRequiredMixin, ListView):
    permission_required = 'post.view_posts'
    raise_exception = False
    permission_denied_message = 'Permissin not set yet!'
    model = Posts
    template_name = "post/list.html"
    context_object_name = 'posts'
    queryset = None
    paginate_by = 5
    ordering = ['-id']

    # def handle_no_permission(self):
    #     messages.error(self.request, 'You have no permission')
    #     return super(PostListView, self).handle_no_permission()

    # custom query
    def get_queryset(self):
        Posts.obj.filter(user=self.request.user, is_active=True)
        # return Posts.obj.filter(user=self.request.user, is_active=True)
        return Posts.obj.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        from django.apps import apps as djagno_apps

        # Phase 1: initialize app configs and import app modules.
        print(djagno_apps.get_app_configs())
        print(djagno_apps.get_app_config('post'))

        # Phase 2: import models modules.
        print(djagno_apps.get_model('post', 'posts', require_ready=True))

        # Phase 3: run ready() methods of app configs.
        print(djagno_apps.ready)

        print(djagno_apps.is_installed('posts'))
        

        data = super().get_context_data(**kwargs)
        data['page_title'] = 'List'
        return data


# DetailView
class PostDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = 'post.view_posts'
    pk = 'id'
    pk_url_kwarg = 'id'
    # slug_field = 'id'
    # slug_url_kwarg = 'id'
    model = Posts
    template_name = "post/details.html"
    context_object_name = 'post_data'

    def get_context_data(self, *args, **kwargs):
        try:
            print('request-user: ', self.request.user)
            print('request-auth: ', self.request.content_type)
            print(467464646464646)
            context = super().get_context_data(*args, **kwargs)
            self.object.views.add(self.request.user)
            context['is_liked'] = True if self.object.likes.filter(id=self.request.user.id).exists() else False
            context['is_disliked'] = True if self.object.dislikes.filter(id=self.request.user.id).exists() else False
            context['no_of_likes'] = self.object.total_likes()
            context['no_of_dislikes'] = self.object.total_dislikes()
            context['no_of_views'] = self.object.total_views()

            query = Comment.objects.filter(post=self.get_object())
            comments = query.filter(parent=None)
            replies = query.exclude(parent=None)

            dic_to_reply = {}
            for reply in replies:
                if reply.parent.id not in dic_to_reply:
                    dic_to_reply[reply.parent.id] = [reply]
                else:
                    dic_to_reply[reply.parent.id].append(reply)

            print(dic_to_reply)
            context['comments'] = comments
            context['replies'] = dic_to_reply
            context['no_of_comments'] = comments.count()
            # context['comment_form'] = CommentForm()
            print(self.get_object().id)
            
            # messages.info(self.request, _("Info: Data loaded successfully"))
            # messages.success(self.request, _("Success: Data loaded successfully"))
            # messages.warning(self.request, _("Warning: Data loaded successfully"))
            # messages.error(self.request, _("Error: Data loaded successfully"))
            # messages.debug(self.request, _("Debug: Data loaded successfully"))
            return context
        except Exception as ex:
            print(ex)
        

#--------------------- LIKE/COMMENT/SHARE
def PostLikeView(request, pk): # Like/Dislike
    post = get_object_or_404(Posts, pk=pk)

    if request.POST.get('like_dislike') == 'like':
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            if post.dislikes.filter(id=request.user.id).exists():
                post.dislikes.remove(request.user)

    elif request.POST.get('like_dislike') == 'dislike':
            if post.dislikes.filter(id=request.user.id).exists():
                post.dislikes.remove(request.user)
            else:
                post.dislikes.add(request.user)
                if post.likes.filter(id=request.user.id).exists():
                    post.likes.remove(request.user)
    else:
        pass

    return HttpResponseRedirect(reverse('post:details', args=[str(pk)]))


class CommentView(CreateView):
    template_name = 'details.html'
    model = Comment
    form_class = CommentForm
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,'You commented successfully')
        return reverse_lazy('post:details', kwargs={'id': self.object.post_id})

    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.post_id = form.data['post_id']
        if form.data['parent']:
            form.instance.parent_id = form.data['parent']
        form.is_active = True
        form.save()
        return super().form_valid(form)



# def PostFormFn(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             pass  # does nothing, just trigger the validation
#     else:
#         form = PostForm()
#     return render(request, 'base_form.html', {'form': form})
