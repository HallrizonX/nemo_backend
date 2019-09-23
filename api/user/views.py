from django.http import HttpRequest, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Profile, BanList, IPlist
from ipware import get_client_ip


class UserObjectAPIVIew(APIView):

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        profile: Profile = Profile.objects.all().last()

        return Response('eee', status=status.HTTP_200_OK)
