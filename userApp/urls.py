from django.urls import path
from .views import kullaniciLogin,kullaniciRegister


urlpatterns = [
    path('kullanicigiris', kullaniciLogin),
    path('kullanicikayit', kullaniciRegister)
]