from django.urls import path
from .views import *

urlpatterns = [
    path('', envia_Email , name='envia_Email'),
]