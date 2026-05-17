import datetime
import strawberry.django
from userApp.models import UserModel
from gorevApp.models import GorevModel
from typing import List, Optional
from dosyaEk.models import DosyaEkModel
from gorselEk.models import GorselEkModel
from sesEk.models import SesEkModel
from videoEk.models import VideoEkModel
from strawberry import auto
from revizeApp.models import RevizeModel
from raporApp.models import RaporModel
from notificationsApp.models import OneSignalApiModel
from asgiref.sync import sync_to_async
from strawberry.types import Info
import typing
from graphql import GraphQLError
from knox.auth import TokenAuthentication


#Knox Authenticated
def getAuthenticatedUser(request):
    try:
        auth = TokenAuthentication()
        user_auth_tuple = auth.authenticate(request)
        if user_auth_tuple is not None:
            user, _ = user_auth_tuple
        else:
            user = request.user  # Knox authenticate None dönerse bile Django'dan deneyelim

        if not user or not user.is_authenticated:
            raise GraphQLError("Giriş Yapınız!")

        return user

    except Exception as e:
        print("Auth error:", str(e))
        raise GraphQLError("Kimlik doğrulama başarısız.")

# Modeller için Typelar
@strawberry.django.type(OneSignalApiModel)
class OneSignalType:
    oneSignalApiId : str

@strawberry.django.type(DosyaEkModel)
class DosyaType:
    id                  : auto
    dosya               : str
    dosyaOlusturmaTarihi: datetime.datetime
    dosyaUzantisi       : str

@strawberry.django.type(VideoEkModel)
class VideoType:
    id                 :auto
    video              :str
    videoYuklenmeTarihi:datetime.datetime
    videoUzantisi      :str

@strawberry.django.type(SesEkModel)
class SesType:
    id               :auto
    ses              :str
    sesYuklenmeTarihi:datetime.datetime
    sesUzantisi      :str

@strawberry.django.type(GorselEkModel)
class GorselType:
    id                  : auto
    resim               : str
    resimOlusturmaTarihi: datetime.datetime
    resimUzantisi       : str


@strawberry.django.type(UserModel)
class UserType:
    userType : str
    firstName: str
    lastName : str
    email    : str


@strawberry.django.type(GorevModel)
class GorevType:
    id                  : auto
    baslik              : str
    aciklama            : str
    gorevDurumu         : str
    gorevOlusturmaTarihi: datetime.datetime
    gorevOlusturan      : Optional[UserType] #null kontrolü için şimdilik deneme aşamasında optional
    gorevDuzenlemeTarihi: datetime.datetime
    gorevDuzenleyen     : UserType
    gorevliler          : List[UserType]
    gorevDosya          : List[DosyaType]
    gorevResim          : List[GorselType]



@strawberry.django.type(RevizeModel)
class RevizeType:
    id                   : auto
    baslik               : str
    aciklama             : str
    revizeDurumu         : str
    aktif                : bool
    oncekiRevize         : typing.Optional["RevizeType"]
    altRevize            : typing.List["RevizeType"] 
    revizeDuzenlemeTarihi: datetime.datetime
    revizeDuzenleyen     : Optional[UserType]  #null kontrolü için şimdilik deneme aşamasında optional
    revizeOlusturmaTarihi: datetime.datetime
    revizeOlusturan      : Optional[UserType]  #null kontrolü için şimdilik deneme aşamasında optional
    gorev                : GorevType
    revizeDosya          : List[DosyaType]
    revizeResim          : List[GorselType]
    revizeKullanicilar   : List[UserType]

    @strawberry.field
    async def revizeRaporlar(self) -> List["RaporType"]:
        raporlar = await sync_to_async(list)(self.raporRevize.all())
        return raporlar



@strawberry.django.type(RaporModel)
class RaporType:
    id                     : auto
    baslik                 : str
    aciklama               : str    
    raporDuzenlemeTarihi   : datetime.datetime
    raporDuzenleyen        : UserType
    raporOlusturmaTarihi   : datetime.datetime
    revizeDurumu           : str
    raporOlusturan         : UserType
    raporRevize            : RevizeType
    raporDosya             : List[DosyaType]
    raporResim             : List[GorselType]
    raporKullanicilar      : List[UserType]



@strawberry.type
class Query:
    @strawberry.field
    def dosyalar(self, info:Info)-> List[DosyaType]:
        return DosyaEkModel.objects.all()
    
    @strawberry.field
    def resimler(self, info:Info)-> List[GorselType]:
        return GorselEkModel.objects.all()
    
    @strawberry.field
    def sesler(self, info:Info)-> List[SesType]:
        return SesEkModel.objects.all()
    
    @strawberry.field
    def videolar(self, info:Info)-> List[VideoType]:
        return VideoEkModel.objects.all()
    


    @strawberry.field
    def gorevler(self, info:Info)-> List[GorevType]:
        request = info.context["request"]
        user = getAuthenticatedUser(request)


        if user is None or not user.is_authenticated:
            raise Exception("Giriş yapınız.")
        
        if user.userType =="yönetici":
            return GorevModel.objects.all()
        gorevler = GorevModel.objects.filter(gorevliler=user)

        if not gorevler:
            raise Exception("Size ait bir görev bulunmuyor")
        
        return gorevler
    
    @strawberry.field
    def revizeler(self, info:Info) -> List[RevizeType]:
        request= info.context["request"]
        user = getAuthenticatedUser(request)

        if user is None or not user.is_authenticated:
            raise Exception("Giriş yapınız.")
        
        if user.userType == "yönetici":
            return RevizeModel.objects.all()
        revizeler = RevizeModel.objects.filter(revizeKullanicilar=user)

        if not revizeler:
            raise Exception("size ait bir revize bulunmuyor")
        
        return revizeler
    
    @strawberry.field
    def raporlar(self, info:Info) -> List[RaporType]:
        request = info.context["request"]
        user = getAuthenticatedUser(request)

        if user is None or not user.is_authenticated:
            raise Exception("Giriş yapınız.")
        
        if user.userType == "yönetici":
            return RaporModel.objects.all()
        # raporKullanıclar içindeyse raporu oluşturmasa bile o raporu görsün
        raporlar = RaporModel.objects.filter(raporKullanicilar=user)

        return raporlar


    @strawberry.field
    async def oneSignalApi(self) -> "OneSignalType":
        ayar = await sync_to_async(lambda: OneSignalApiModel.objects.first())()
        if ayar:
            return OneSignalType(oneSignalApiId=ayar.oneSignalApiId)
        return OneSignalType(oneSignalApiId="")