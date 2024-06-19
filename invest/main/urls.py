from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name = 'main'),
    path('count', views.count, name = 'count'),
    path('data', views.data, name = 'data'),
]
