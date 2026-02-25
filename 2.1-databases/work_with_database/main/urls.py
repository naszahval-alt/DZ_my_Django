from django.contrib import admin
from django.urls import path
from phones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', views.show_catalog, name='show_catalog'),
    path('catalog/<slug:slug>/', views.phone_detail, name='phone'),
]
