from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from gorevApp.models import GorevModel
from revizeApp.models import RevizeModel
from dosyaEk.models import DosyaEkModel
from gorselEk.models import GorselEkModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=GorevModel)
def createRevizeForGorev(sender,instance,created,**kwargs):
    if created:
        revize = RevizeModel.objects.create(
            baslik=instance.baslik,
            aciklama=instance.aciklama,
            gorev=instance,
            revizeOlusturan=instance.gorevOlusturan,
            revizeDuzenleyen=instance.gorevDuzenleyen,
        )
        revize.revizeDosya.set(instance.gorevDosya.all())
        revize.revizeResim.set(instance.gorevResim.all())
        revize.revizeKullanicilar.set(instance.gorevliler.all())


@receiver(m2m_changed, sender=GorevModel.gorevliler.through)
def sync_gorev_gorevliler_with_revize(sender, instance, action, **kwargs):
    if action == "post_add":
        try:
            revize = RevizeModel.objects.get(gorev=instance)
            revize.revizeKullanicilar.set(instance.gorevliler.all())
        except RevizeModel.DoesNotExist:
            pass

@receiver(m2m_changed, sender=GorevModel.gorevDosya.through)
def sync_gorev_gorevDosya_with_revize(sender, instance, action, **kwargs):
    if action == "post_add":
        try:
            revize = RevizeModel.objects.get(gorev=instance)
            revize.revizeDosya.set(instance.gorevDosya.all())
        except RevizeModel.DoesNotExist:
            pass

@receiver(m2m_changed, sender=GorevModel.gorevResim.through)
def sync_gorev_gorevResim_with_revize(sender, instance, action, **kwargs):
    if action == "post_add":
        try:
            revize = RevizeModel.objects.get(gorev=instance)
            revize.revizeResim.set(instance.gorevResim.all())
        except RevizeModel.DoesNotExist:
            pass



@receiver(post_save, sender=RevizeModel)
def revizeOnayForGorev(sender,instance,created,**kwargs):
    if not created and instance.revizeDurumu == 'revizeOnaylandi':
        gorev = instance.gorev
        if gorev.gorevDurumu != 'gorevOnaylandi':
            gorev.gorevDurumu = 'gorevOnaylandi'
            gorev.save()

@receiver(post_save, sender=RevizeModel)
def revizeIptalForGorev(sender,instance,created,**kwargs):
    if not created and instance.revizeDurumu == 'revizeIptal':
        gorev = instance.gorev
        if gorev.gorevDurumu != 'gorevIptal':
            gorev.gorevDurumu = 'gorevIptal'
            gorev.save()


@receiver(m2m_changed, sender=GorevModel.gorevliler.through)
def notify_users_on_task_assign(sender, instance, action, pk_set, **kwargs):
    # Sadece görevliler eklendiğinde çalışsın
    if action == "post_add":
        channel_layer = get_channel_layer()
        
        # Eklenen her bir kullanıcının ID'sini (pk_set) döngüye al
        for user_id in pk_set:
            group_name = f"user_{user_id}"
            
            # O kullanıcının WebSocket odasına mesaj gönder
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_notification', # Consumer'daki metodun adı
                    'message': f"Yeni bir görev atandı: {instance.baslik}"
                }
            )