from django.db import models
import os
from django.core.exceptions import ValidationError

VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv', 'webm']

def validateVideoExtensions(value):
    ext = os.path.splitext(value.name)[1]
    if ext:
        ext = ext.lower().lstrip('.')
    if ext not in VIDEO_EXTENSIONS:
        raise ValidationError(f"{ext} Bu video uzantısı desteklenmiyor. Bu uzantılı videoları yükleyebilirsiniz: {VIDEO_EXTENSIONS}")
    
def validateVideoSize(value):
    limit = 50 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("Dosya boyutu çok büyük. Max dosya boyutu: 50MB")

class VideoEkModel(models.Model):
    video               = models.FileField(upload_to='videolar/',validators=[validateVideoExtensions,validateVideoSize])
    videoYuklenmeTarihi = models.DateTimeField(auto_now_add=True)
    videoUzantisi       = models.CharField(max_length=15,blank=True)

    def save(self,*args,**kwargs):
        if self.video and not self.videoUzantisi:
            name, extension =os.path.splitext(self.video.name)
            self.videoUzantisi =extension.lower().lstrip('.')
        super().save(*args, **kwargs)

        def __str__(self):
            return self.video.name
