from django.urls import path
from session_cookie_cache.views import SetTemplateView, GetTemplateView, ListTemplateView, DeleteTemplateView, FlusDeleteTemplateView

app_name = 'session_cookie_cache'

urlpatterns = [
    path('set/', SetTemplateView.as_view(), name='set'),
    path('details/<str:_key>/', GetTemplateView.as_view(), name='details'),
    path('list/', ListTemplateView.as_view(), name='list'),
    path('delete/<str:_key>/', DeleteTemplateView.as_view(), name='delete'),
    path('flus-delete/', FlusDeleteTemplateView.as_view(), name='flus_delete'),
]
