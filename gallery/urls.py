from django.urls import path

from .views import style_list, tattoo_detail_view, tattoos_view

app_name = 'gallery'

urlpatterns = [
    path('', tattoos_view, name='tattoos'),
    path('<slug:slug>/', tattoo_detail_view, name='tattoo-detail'),
    path('search/<slug:slug>/', style_list, name='style-list'),
]
