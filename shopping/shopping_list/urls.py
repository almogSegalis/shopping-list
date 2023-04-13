
from django.urls import path
from . import views

app_name = 'shopping_list'

urlpatterns = [
    path('', views.main_shopping_list, name="list"),
    path('add_item/<item_name>', views.add_item, name='add_item'),
    path('delete_item/<item_id>', views.delete_item, name="delete_item"),
    path('item_list/<tag_name>', views.main_shopping_list ,name="item_list_by_tag"),
    path('get-items/', views.get_items, name='get_items'),
    path('filter_items/<tag_name>/', views.filter_items, name='filter_items'),
    path('update_quantity/<item_id>/<quantity>', views.update_quantity, name='update_quantity'),
]