from django.db import models
import os
from django.core.exceptions import ValidationError


DOSYA_EXTENCIONS ={'pdf', 'docx', 'doc', 'xlsx', 'pptx'}

def validateFileExtension(value):
    ext = os.path.splitext(value.name)[1]
    if ext:
        ext = ext.lower().lstrip('.')
    if ext not in DOSYA_EXTENCIONS:
        raise ValidationError(f'{ext} uzantılı dosylar desteklenmiyor. Sadece şu uzantılı dosyalar ekelenebilir: {DOSYA_EXTENCIONS}')

class DosyaEkModel(models.Model):
    dosya               = models.FileField(upload_to='dosyalar/',validators=[validateFileExtension])
    dosyaOlusturmaTarihi= models.DateTimeField(auto_now_add=True)
    dosyaUzantisi       = models.CharField(max_length=15,blank=True)

    def save(self, *args,**kwargs):
        if self.dosya and not self.dosyaUzantisi:
            name, extension=os.path.splitext(self.dosya.name)
            self.dosyaUzantisi =extension.lower().lstrip('.')
        super().save(*args, **kwargs)


    def __str__(self):
        return self.dosya.name
    
