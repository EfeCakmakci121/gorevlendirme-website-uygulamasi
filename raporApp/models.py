from django.db import models
from revizeApp.models import RevizeModel
from dosyaEk.models import DosyaEkModel
from gorselEk.models import GorselEkModel
from userApp.models import UserModel

class RaporModel(models.Model):
    baslik               = models.CharField(max_length=150)
    aciklama             = models.CharField(max_length=150)
    raporRevize          = models.ForeignKey(RevizeModel, on_delete=models.CASCADE, related_name='raporRevize')
    raporResim           = models.ManyToManyField(GorselEkModel, blank=True, related_name='raporResimler')
    raporDosya           = models.ManyToManyField(DosyaEkModel, blank=True, related_name='raporDosyalar')
    raporOlusturmaTarihi = models.DateTimeField(auto_now_add=True)
    raporOlusturan       = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='raporOlusturan')
    raporDuzenlemeTarihi = models.DateTimeField(auto_now=True)
    raporDuzenleyen      = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='raporDuzenleyen')
    raporKullanicilar    = models.ManyToManyField(UserModel, blank=True,related_name='raporKullanicilar')

 