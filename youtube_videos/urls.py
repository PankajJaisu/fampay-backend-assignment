from django.urls import path
from .views import *

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
]
