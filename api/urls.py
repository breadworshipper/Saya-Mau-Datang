
from django.urls import path, include
from . import views

urlpatterns = [
    path('query_by_model', views.search_query_by_model, name='search_query_by_model'),
    path('query_by_manufacturer', views.search_query_by_manufacturer, name='search_query_by_manufacturer'),
]