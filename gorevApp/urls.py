from django.urls import path
from .views import onesignalTest,gorevlerim,gorevOlustur


urlpatterns = [
    path('onesignal-test/', onesignalTest),
    path('gorevlerim/', gorevlerim),
    path('gorevolustur/', gorevOlustur),
]
