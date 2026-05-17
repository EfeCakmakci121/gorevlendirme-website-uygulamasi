from django.db import models
import os
from django.core.exceptions import ValidationError

AUDIO_EXTENSIONS = ['mp3','wav','ogg','flac','m4a','aac','wma','aiff',]

def validateSesExtensions(value):
    ext = os.path.splitext(value.name)[1]
    if ext:
        ext = ext.lower().lstrip('.')
    if ext not in AUDIO_EXTENSIONS:
        raise ValidationError(f"{ext} ses uzantısı desteklenmiyor. Bu uzantıya sahip dosyaları yükleyiniz: {AUDIO_EXTENSIONS}")



class SesEkModel(models.Model):
    ses               = models.FileField(upload_to='ses/',validators=[validateSesExtensions])
    sesYuklenmeTarihi = models.DateTimeField(auto_now_add=True)
    sesUzantisi       = models.CharField(max_length=15,blank=True)

    def save(self,*args,**kwargs):
        if self.ses and not self.sesUzantisi:
            name,extension = os.path.splitext(self.ses.name)
            self.sesUzantisi = extension.lower().lstrip('.')
        super().save(*args,**kwargs)

    def __str__(self):
        return self.ses.name