
from django.urls import path
from . import views

app_name = 'shopping_list'

urlpatterns = [
    path('', views.main_shopping_list, name="list"),
    path('add_item', views.add_item, name="add_item"),
    path('delete_item/<item_id>', views.delete_item, name="delete_item"),
    path('item_list/<tag_name>', views.main_shopping_list ,name="item_list_by_tag"),
    path('get-items/', views.get_items, name='get_items'),
]