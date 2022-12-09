"""awoosome_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.i18n import i18n_patterns
import debug_toolbar

from .views import error_403, error_404, error_500


urlpatterns = [
    # path('admin/', include('post.admin_urls', namespace="admin")),
    path('', include('awoosome_django.api_urls'))
]

urlpatterns += i18n_patterns(
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("users/", include("users.urls", namespace="users")),
    path('post/', include('post.urls', namespace="post")),
    path('film/', include('film.urls', namespace="film")),
    path('session/', include('session_cookie_cache.urls',
         namespace="session_cookie_cache")),
    # path('proxy/', include('proxy_app.urls', namespace="proxy")),
    
    path('__debug__/', include('debug_toolbar.urls')),
)

#---- Custom error page

# handler400 = error_400 # bad request
handler403 = error_403 # permission denied
handler404 = error_404 # page not found
handler500 = error_500 # server error

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
