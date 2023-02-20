
from django.urls import path
from . import views

app_name = 'shopping_list'

urlpatterns = [
    path('', views.main_shopping_list, name="list"),
    path('add/', views.add_item, name="add"),
    path('delete_item/<item_id>', views.delete_item, name="delete_item")
]