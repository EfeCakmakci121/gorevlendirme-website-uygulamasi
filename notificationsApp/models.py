from django.db import models


class OneSignalApiModel(models.Model):
    oneSignalApiId  = models.CharField(max_length=255)
    oneSignalApiKey = models.CharField(max_length=255)

    def __str__(self):
        return "OneSignal Ayarı"
