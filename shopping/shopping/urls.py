from django.contrib import admin
from django.urls import path, include
from shopping_list import views as shopping_list_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('shopping_list/', include('shopping_list.urls')),
    path("admin/", admin.site.urls),
    path("", shopping_list_view.main_shopping_list, name="home"),
]

urlpatterns += staticfiles_urlpatterns()
