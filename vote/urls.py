from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('cast/', views.cast_vote, name='cast-vote'),
    path('get-ministry', views.get_ministry, name='get-ministry')
]
