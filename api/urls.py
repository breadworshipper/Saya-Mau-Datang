
from django.urls import path, include
from . import views

urlpatterns = [
    path('query', views.search_query, name='search_query'),
]