from django.http import JsonResponse
from django.views.decorators import http
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import random
import string
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Custom token
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['is_staff'] = user.is_staff

        return token

    # Custom data
    def validate(self, attrs):
        data = super().validate(attrs)
        # token = self.get_token(self.user)
        data['type'] = str(settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0]) # 'Bearer'
        data['lifetime'] = str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days) + ' days'

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# @login_required
# @http.require_http_methods(['GET'])
# def api_without_drf(request):
#     letters = string.ascii_letters
#     data=[random.choice(letters) for i in range(10)]
#     return JsonResponse({'data': data})


@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
@api_view(['GET'])
def api_drf(request):
    letters = string.ascii_letters
    data = [random.choice(letters) for i in range(10)]
    return Response({'data': data})
    
