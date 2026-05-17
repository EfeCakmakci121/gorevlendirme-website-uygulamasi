from django.db import models
from dosyaEk.models import DosyaEkModel
from gorselEk.models import GorselEkModel
from userApp.models import UserModel

class GorevModel(models.Model):
    baslik              = models.CharField(max_length=150)
    aciklama            = models.CharField(max_length=350)
    gorevDosya          = models.ManyToManyField(DosyaEkModel, blank=True, related_name='dosyalar')
    gorevResim          = models.ManyToManyField(GorselEkModel, blank=True, related_name='resimler')
    gorevliler          = models.ManyToManyField(UserModel, blank=True, related_name='görevliler')
    gorevOlusturan      = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='gorevOlusturan')
    gorevOlusturmaTarihi= models.DateTimeField(auto_now_add=True)
    gorevDuzenlemeTarihi= models.DateTimeField(auto_now=True)
    gorevDuzenleyen     = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='gorevDuzenleyen')
    gorevDurumu         = models.CharField(default="Görev Atandı", max_length=50, choices=[
        ('gorevAtandi','Gorev Atandı.'),
        ('gorevIptal','Görev İptal'),
        ('gorevOnayBekleniyor','Görev Onay Bekleniyor'),
        ('gorevOnaylandi','Görev Onaylandı')
    ])

    def __str__(self):
        return f"{self.baslik} {self.gorevDurumu}"