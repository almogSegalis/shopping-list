
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_shopping_list),
]