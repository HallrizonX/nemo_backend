from collections import namedtuple
from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

AuthLinks = namedtuple('AuthLinks', 'auth verify refresh')
auth_links = AuthLinks(
    'v1/auth/',
    'v1/refresh/',
    'v1/verify/'
)

jwt_patterns = [
    path(auth_links.auth, obtain_jwt_token),
    path(auth_links.refresh, refresh_jwt_token),
    path(auth_links.verify, verify_jwt_token)
]

urlpatterns = [
    *jwt_patterns,
    path('v1/users/', include('api.user.urls'))
]
