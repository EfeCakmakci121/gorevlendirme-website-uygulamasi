import os
from django.db import models
from django.core.exceptions import ValidationError


GORSEL_EXTENCIONS=['jpg','jpeg','png','gif','bmp','tiff','tif','webp','heic',]

def ValidateImageExtencions(value):
    ext = os.path.splitext(value.name)[1]
    if ext:
        ext =ext.lower().lstrip('.')
    if ext not in GORSEL_EXTENCIONS:
        raise ValidationError(f"{ext} uzantılı resimler yüklenemiyor. Sadece bu uzantılı resimleri yükleyebilirsiniz: {GORSEL_EXTENCIONS}")



class GorselEkModel(models.Model):
    resim               = models.ImageField(upload_to='resimler/',validators=[ValidateImageExtencions])
    resimOlusturmaTarihi= models.DateTimeField(auto_now_add=True)
    resimUzantisi       = models.CharField(max_length=15,blank=True)

    def save(self,*args,**kwargs):
        if self.resim and not self.resimUzantisi:
            name, extension=os.path.splitext(self.resim.name)
            self.resimUzantisi =extension.lower().lstrip('.')
        super().save(*args, **kwargs)



    def __str__(self):
        return self.resim.name
