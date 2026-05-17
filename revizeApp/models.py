from django.db import models
from dosyaEk.models import DosyaEkModel
from gorselEk.models import GorselEkModel
from gorevApp.models import GorevModel
from userApp.models import UserModel


class RevizeModel(models.Model):
    baslik               = models.CharField(max_length=150)
    aciklama             = models.CharField(max_length=350)
    revizeResim          = models.ManyToManyField(GorselEkModel, blank=True, related_name='revizeResimler')
    revizeDosya          = models.ManyToManyField(DosyaEkModel, blank=True, related_name='revizeDosyalar')
    gorev                = models.ForeignKey(GorevModel,on_delete=models.CASCADE,related_name='revizeGorevler')
    revizeKullanicilar   = models.ManyToManyField(UserModel, blank=True,related_name='revizeKullanicilar')
    revizeOlusturmaTarihi= models.DateTimeField(auto_now_add=True)
    revizeOlusturan      = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='revizeOlusturanlar')
    revizeDuzenlemeTarihi= models.DateTimeField(auto_now=True)
    revizeDuzenleyen     = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='revizeDuzenleyenler')
    oncekiRevize         = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="altRevize")
    aktif                = models.BooleanField(default=True)
    revizeDurumu         =models.CharField(default="Revize Rapor Bekleniyor.", max_length=50, choices=[
        ('revizeRaporBekleniyor','Revize Rapor Bekleniyor'),
        ('revizeIptal','Revize İptal'),
        ('revizeGuncellendi', 'Revize Güncellendi'),
        ('revizeOnayBekleniyor','Revize Onay Bekleniyor'),
        ('revizeOnaylandi','Revize Onaylandı')
    ])

    def __str__(self):
        return f"{self.baslik} {self.revizeDurumu}"