from django.urls import path
from .views import raporlarim,raporOlustur,raporGuncelle


urlpatterns = [
    path('raporlarim/', raporlarim),
    path('rapor-olustur/', raporOlustur),
    path('rapor-guncelle' ,raporGuncelle)
]