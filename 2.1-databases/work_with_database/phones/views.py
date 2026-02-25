from django.shortcuts import render, get_object_or_404
from .models import Phone

def show_catalog(request):
    """Отображает каталог телефонов с сортировкой."""
    sort_param = request.GET.get('sort', 'name')

    sort_mapping = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price',
    }
    sort_field = sort_mapping.get(sort_param, 'name')
    phones = Phone.objects.all().order_by(sort_field)

    context = {
        'phones': phones,
        'current_sort': sort_param
    }
    return render(request, 'catalog.html', context)

def phone_detail(request, slug):
    """Отображает детальную информацию о телефоне."""
    phone = get_object_or_404(Phone, slug=slug)
    context = {'phone': phone}
    return render(request, 'phone_detail.html', context)
