from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .managers import UserManager


class IPlist(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.ip


class Profile(models.Model):
    objects = UserManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IP_list = models.ManyToManyField(IPlist, blank=True)

    class Meta:
        db_table = 'profile'


class BanList(models.Model):
    ip = models.ForeignKey(IPlist, blank=True, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Profile, blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.ip} or {self.user}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
