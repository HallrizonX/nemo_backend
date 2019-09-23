import re

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ipware import get_client_ip

from api.urls import auth_links

from .models import BanList, IPlist


class VerifyIPAndUserBanList:
    """
    Class for checkout BanList by IP or User from request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if VerifyIPAndUserBanList.is_free_link(link=request.get_full_path()):

            ip, is_routable = get_client_ip(request)
            user: User = VerifyIPAndUserBanList.get_user_from_request(request)

            if BanList.objects.only(ip).filter(ip__ip=ip).count() >= 1 or \
                    BanList.objects.filter(user__user=user).count() >= 1:
                return HttpResponse(status=403)
            else:
                VerifyIPAndUserBanList.assign_ip_to_user(ip, user)

        response: HttpResponse = self.get_response(request)

        return response

    @staticmethod
    def assign_ip_to_user(ip, user: User):
        """
        Checkout if IP address from request is in DataBase and that IP address adding to current user
        :param ip:
        :param user:
        :return None:
        """
        _ip, create_ip = IPlist.objects.get_or_create(ip=ip)
        if create_ip:
            user.profile.IP_list.add(IPlist.objects.get(ip=ip))
            user.profile.save()
        else:
            if not user.profile.IP_list.filter(ip=ip).count() >= 1:
                user.profile.IP_list.add(IPlist.objects.get(id=_ip.id))

    @staticmethod
    def get_user_from_request(request):
        """
        Getting user from User table
        :param request:
        :return User or None:
        """
        JWT = JSONWebTokenAuthentication()
        user, payload = JWT.authenticate(request)
        return user if user else None

    @staticmethod
    def is_free_link(link) -> bool:
        """
        Checkout if url from request is valid
        :param link:
        :return True or False:
        """
        free_links = [f'/api/{_link}' for _link in auth_links]
        # if user enter to admin panel. That use any verify
        try:
            free_links.append(re.match('/admin/', link).string)
        except AttributeError:
            pass

        return True if link not in free_links else False
