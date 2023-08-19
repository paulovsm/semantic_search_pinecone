from django.urls import path

from .views import hello,search

urlpatterns = [
    path('', hello, name='hello'),
    path('search', search, name='search'),
]