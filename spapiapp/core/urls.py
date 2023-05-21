from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('artist_stats/',views.artist_stats, name='artist_stats')
]
