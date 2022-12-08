from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    path('list/', views.FilmListView.as_view(), name='film-list'),
    # path('films/<int:pk>/detail', views.FilmCreateView.as_view(), name='film_detail'),
    path('create/', views.FilmCreateView.as_view(), name='film_create'),
    path('<int:pk>/update/', views.FilmUpdateView.as_view(), name='film_update'),
    path('<int:pk>/delete/', views.FilmDeleteView.as_view(), name='film_delete'),
]
