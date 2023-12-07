
from django.urls import path, include
from . import views

urlpatterns = [
    path('query_by_model', views.search_query_by_model, name='search_query_by_model'),
    path('query_by_manufacturer', views.search_query_by_manufacturer, name='search_query_by_manufacturer'),
    path('detail/<str:car_id>', views.get_detail_by_id, name='detail'),
    path('query_by_price_range', views.search_query_by_price_range, name='search_query_by_price_range'),
    path('query_by_category', views.search_query_by_category, name='search_query_by_category'),
]