from django.contrib import admin
from gorevApp.models import GorevModel
from revizeApp.models import RevizeModel
from raporApp.models import RaporModel
from dosyaEk.models import DosyaEkModel
from gorselEk.models import GorselEkModel

# Register your models here.

admin.site.register(GorevModel)
admin.site.register(RevizeModel)
admin.site.register(RaporModel)
admin.site.register(DosyaEkModel)
admin.site.register(GorselEkModel)


