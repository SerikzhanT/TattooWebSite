from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from gallery.models import TattooProxy


def appointment(request):
    return render(request, 'appointment/appointment.html')
