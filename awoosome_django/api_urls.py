from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from .api.v1.viewsets import CustomTokenObtainPairView

from .api.v1.viewsets import api_drf

urlpatterns = [
    path('api/v1/', include([
        path('login/', obtain_auth_token),
        path('jwt-login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
         path('jwt-login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('', include('rest_framework.urls')),
        # path('api-without-drf/', api_without_drf),
        path('api-drf/', api_drf),
    ])),
]