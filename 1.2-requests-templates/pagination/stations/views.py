from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv
from pagination.settings import BUS_STATION_CSV

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(BUS_STATION_CSV, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        bus_stations_list = list(reader)
        paginator = Paginator(bus_stations_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'bus_stations': page_obj,
            'page': page_obj,
        }

    return render(request, 'stations/index.html', context)
