from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.signals import request_finished


from .models import Film
from .forms import FilmForm


class FilmBaseView(View):
    model = Film
    fields = '__all__'
    success_url = reverse_lazy('films:all')


class FilmListView(FilmBaseView, ListView):

    template_name = 'film/list.html'
    context_object_name = 'films-obf'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(FilmListView, self).get_context_data(**kwargs)
        films = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(films, self.paginate_by)
        try:
            films = paginator.page(page)
        except PageNotAnInteger:
            films = paginator.page(1)
        except EmptyPage:
            films = paginator.page(paginator.num_pages)
        context['films'] = films
        return context


class FilmCreateView(CreateView): 
    template_name = 'base_form.html'
    form_class = FilmForm
    success_url = '.'
    # success_url = reverse_lazy('film/list')


# class FilmCreateView(FilmBaseView, CreateView):
#     """View to create a new film"""


class FilmUpdateView(FilmBaseView, UpdateView):
    """View to update a film"""


class FilmDeleteView(FilmBaseView, DeleteView):
    """View to delete a film"""
