from django.contrib import admin
from .models import Profile, BanList, IPlist

admin.site.register(Profile)
admin.site.register(BanList)
admin.site.register(IPlist)
