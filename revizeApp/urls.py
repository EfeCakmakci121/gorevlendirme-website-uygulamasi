from django.urls import path
from .views import revizelerim,revizeGuncelleme


urlpatterns = [
    path('revizelerim/', revizelerim),
    path('revize-guncelleme', revizeGuncelleme),
]