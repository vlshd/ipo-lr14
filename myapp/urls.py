from django.urls import path
from .views import *

urlpatterns = [
    path('', hello_world, ),
    path('about/', about, name='about'),
    path('aboutShop/', aboutShop, name='aboutShop'),
]