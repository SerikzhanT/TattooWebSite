from django.shortcuts import get_object_or_404, render

from .models import Style, TattooProxy


def tattoos_view(request):
    tattoos = TattooProxy.objects.all()
    return render(request, 'gallery/tattoos.html', {'tattoos': tattoos})


def tattoo_detail_view(request, slug):
    tattoo = get_object_or_404(TattooProxy, slug=slug)
    return render(request, 'gallery/tattoo_detail.html', {'tattoo': tattoo})


def style_list(request, slug):
    style = get_object_or_404(Style, slug=slug)
    tattoos = TattooProxy.objects.select_related('style').filter(style=style)
    context = {
        'style': style,
        'tattoos': tattoos
    }
    return render(request, 'gallery/style_list.html', context)
