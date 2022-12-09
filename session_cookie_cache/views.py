from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy


class SetTemplateView(TemplateView):
    template_name = 'session_cookie_cache/set.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['my_user'] = 'Al Amin Raju' 
        self.request.session['auth_username'] = self.request.user.username
        # self.request.session.set_expiry(20)
        context['msg'] = 'Session set succussfully.'

        return context


class ListTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'session_cookie_cache/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msg'] = 'Session list view.'

        return context


class GetTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'session_cookie_cache/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _key = kwargs['_key']
        get_session_by_key = None
        if _key and self.request.session.has_key(_key):
            get_session_by_key = self.request.session.get(_key)

        context['session_key'] = _key
        context['get_session_by_key'] = get_session_by_key
        context['msg'] = 'Get session details.'

        return context


class DeleteTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'session_cookie_cache/list.html'
    success_url = reverse_lazy('post:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _key = kwargs['_key']
        if _key and self.request.session.has_key(_key):
            del self.request.session[_key]
        context['msg'] = 'Session delete successfully.'

        return context


class FlusDeleteTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'session_cookie_cache/list.html'
    success_url = reverse_lazy('post:home')

    def get_context_data(self, **kwargs):
        # from django.contrib.auth import logout
        # logout(self.request)
        context = super().get_context_data(**kwargs)
        self.request.session.flush()
        context['msg'] = 'Session flush successfully.'

        return context



