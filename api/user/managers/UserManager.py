from django.db import models
from django.core.validators import validate_email

from api.user.models import User


class UsernameIsAlreadyInDataBase(Exception):
    pass


class EmailIsAlreadyInDataBase(Exception):
    pass


class EmailIsNotValid(Exception):
    pass


class UserManager(models.Manager):
    user: User

    def valid_username(self, username: str):
        if User.objects.filter(username=username).count() >= 1:
            raise UsernameIsAlreadyInDataBase
        return True

    def valid_email(self, email: str):
        if User.objects.filter(email=email).count() >= 1:
            raise EmailIsAlreadyInDataBase

        if validate_email(email):
            raise EmailIsNotValid
        return True

    def update(self, profile, **kwargs):
        user_fields: list = ['username', 'email']
        profile_fields: list = []

        response: dict = {}

        for key, val in kwargs.items():
            if key in user_fields:
                if getattr(self, f'valid_{key}')(val):
                    profile.user.__setattr__(key, val)
                    response[key] = True

        profile.user.save()

        return response
