from django.urls import path

from .views import appointment

app_name = 'appointment'

urlpatterns = [
    path('', appointment, name='appointment'),
]
