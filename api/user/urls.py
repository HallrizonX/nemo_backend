from django.urls import path
from .views import UserObjectAPIVIew
urlpatterns = [
    path('<str:slug>/', UserObjectAPIVIew.as_view())
]
