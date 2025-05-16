from django.urls import path # type: ignore

from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('menu/<str:item_name>/', view_menu, name='active_item')
]