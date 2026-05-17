from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RaporModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from revizeApp.models import RevizeModel

@receiver(post_save,sender=RaporModel)
def updateGorevDurumuOnRapor(sender,instance,created,**kwargs):
    if not created:
        return
    
    revize = instance.raporRevize
    gorev = revize.gorev

    gorevliler=gorev.gorevliler.all()
    raporYazanlar = set(
        RaporModel.objects.filter(raporRevize__gorev=gorev)
        .values_list("raporOlusturan_id",flat=True)
    )


    if all(user.id in raporYazanlar for user in gorevliler):
        gorev.gorevDurumu = "onayBekleniyor"
        gorev.save()




@receiver(post_save, sender=RaporModel)
def updateTarihForRevize(sender,instance,created,**kwargs):
    revize = instance.raporRevize
    if revize:
        revize.revizeDuzenlemeTarihi = now()
        revize.save()