from django.urls import path

from .views import hello,search
from .personal_stylist_view import recommendation,generateImage

urlpatterns = [
    path('', hello, name='hello'),
    path('search', search, name='search'),
    path('recommendation', recommendation, name='recommendation'),
    path('generateImage', generateImage, name='generateImage'),
]