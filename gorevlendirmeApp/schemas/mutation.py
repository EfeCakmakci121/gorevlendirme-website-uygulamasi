from typing import List,Optional
import strawberry
from knox.models import AuthToken
from strawberry.types import Info
from userApp.models import UserModel
from gorevApp.models import GorevModel
from dosyaEk.models import DosyaEkModel
from gorselEk.models import GorselEkModel
from raporApp.models import RaporModel
from revizeApp.models import RevizeModel
from strawberry import auto
from asgiref.sync import sync_to_async,async_to_sync
from .schema import GorevType,Query,RaporType,RevizeType
from notificationsApp.utils import sendOnesignalMessages
from channels.layers import get_channel_layer
from .subscription import Subscription
import re
from graphql import GraphQLError
from knox.auth import TokenAuthentication
from django.db import transaction
from datetime import datetime
import datetime
import json


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



def safe_group_name(email: str) -> str:
    email = email.lower()
    email = re.sub(r'[^a-z0-9]', '_', email)
    return f"gorev_kullanicilar{email}"

def authenticateUser(email:str,password:str):
    try:
        user= UserModel.objects.get(email=email)
        if user.check_password(password):
            return user
    except UserModel.DoesNotExist:
        return None


# İnput alanları
@strawberry.input
class GorevInput:
    baslik    : str
    aciklama  : str
    gorevliler: List[str] = strawberry.field(default_factory=list)
    gorevDosya: List[int] = strawberry.field(default_factory=list)
    gorevResim: List[int] = strawberry.field(default_factory=list)

@strawberry.input
class RaporInput:
    baslik            : str
    aciklama          :str
    raporRevize       :int
    raporDosya        : List[int] = strawberry.field(default_factory=list)
    raporResim        : List[int] = strawberry.field(default_factory=list)
    raporKullanicilar : Optional[list[str]] = strawberry.field(default_factory=list)

@strawberry.input
class RaporGuncelleInput:
    id:int
    baslik:Optional[str] = None
    aciklama:Optional[str] = None
    raporDosyaId:Optional[List[int]] = None
    raporResimId:Optional[List[int]] = None


# Response alanları
@strawberry.type
class Loginresponse:
    token    :str
    userId   :int
    email    :str
    firstName:str
    lastName :str
    userType :str

@strawberry.type
class RegisterResponse:
    email:str
    firstName:str
    lastName :str
    userType :str



# Mutation alanları
@strawberry.type
class Mutation:
    @strawberry.mutation
    def kullaniciLogin(self, info:Info,email:str,password:str) -> Loginresponse:
        user= authenticateUser(email,password)
        if not user:
            raise Exception("Hatalı şifre veya mail! ")
        
        token= AuthToken.objects.create(user)[1]
        return Loginresponse(token=token,userId=user.id,email=user.email,firstName=user.firstName, lastName=user.lastName, userType=user.userType)
    
    @strawberry.mutation
    def kullaniciRegister(
        self,
        info:Info,
        email:str,
        firstName:str,
        lastName:str,
        password:str,
        userType:str ='personel',
    ) -> RegisterResponse:
        
        user = UserModel.objects.create_user(
            email=email,
            password=password,
            firstName=firstName,
            lastName=lastName,
            userType=userType,
        )

        token= AuthToken.objects.create(user)[1]()

        return RegisterResponse(
            email=user.email,
            firstName=user.firstName,
            lastName=user.lastName,
            userType=user.userType,
        )


    @strawberry.mutation
    def createGorev(self, info:Info, input:GorevInput) -> GorevType:
        request = info.context["request"]
        user = getAuthenticatedUser(request)
        if not user.is_authenticated:
            raise Exception("Giriş yapmış kullanıcı gerekli")
        if user.userType != "yönetici":

            raise Exception("Bu işlem için yönetici hesabına giriş yapmalısınız.")
        
        kayitliKullanicilar = set(UserModel.objects.values_list('email', flat=True))
        inputEmails = set(input.gorevliler)
        hataliMails = inputEmails - kayitliKullanicilar
        if hataliMails:
            raise Exception(f"{', '.join(hataliMails)} Maili sistemde kayıtlı değil")
        

        
        Gorev_obj = GorevModel(
        baslik = input.baslik,
        aciklama = input.aciklama,
        gorevOlusturan = user,
        gorevDuzenleyen = user,
        )
        Gorev_obj.save()

        if not input.gorevliler:
            raise Exception("Görevliler listesi boş olamaz")
        input.gorevliler = set(input.gorevliler)




        users = UserModel.objects.filter(email__in=input.gorevliler)
        Gorev_obj.gorevliler.set(users)


        if input.gorevDosya:
            dosyalar = DosyaEkModel.objects.filter(id__in=input.gorevDosya)

            Gorev_obj.gorevDosya.set(dosyalar)
    
        if input.gorevResim:
            resimler = GorselEkModel.objects.filter(id__in=input.gorevResim)

            Gorev_obj.gorevResim.set(resimler)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gorev_bildirimleri",
            {
                "type": "gorev_message",
                "text": json.dumps({
                    "id": Gorev_obj.id,
                    "baslik": Gorev_obj.baslik,
                    "aciklama": Gorev_obj.aciklama,
                    "gorevOlusturmaTarihi": str(Gorev_obj.gorevOlusturmaTarihi)
                })
            }
        )


        return Gorev_obj
    



    @strawberry.mutation
    def createRapor(self, info:Info, input:RaporInput) -> RaporType:
        request = info.context["request"]
        user = getAuthenticatedUser(request)
        if not user.is_authenticated:
            raise Exception("Giriş yapmış kullanıcı gerekli")
        
        if not input.raporRevize:
            raise Exception("Revize ID belirtilmek zorundadır.")
        
        def get_revize_and_gorev(revize_id):
            revize = RevizeModel.objects.select_related("gorev").get(id=revize_id)
            gorev = revize.gorev
            gorevliler = list(gorev.gorevliler.all())
            return revize, gorev, gorevliler

        revize, gorev, gorevliler = get_revize_and_gorev(input.raporRevize)

        if revize.revizeDurumu == "revizeGuncellendi":
            raise Exception("Bu revize şuanda güncel değil, yeni bir revize atanmış")

        if user not in gorevliler:
            raise Exception("Bu revizeye rapor yazmak için revizede görevli olmalısnız.")
        
        #daha önce rapor atmış mı
        varMi = RaporModel.objects.filter(raporRevize=revize,raporOlusturan=user).exists()
        if varMi:
            raise Exception("Bu revizeye daha önce rapor yazdınız.")
        


        if input.raporKullanicilar:
            emailListesi = input.raporKullanicilar.copy()
            gorevliEmailListesi = set(gorev.gorevliler.values_list("email", flat=True))

            for email in emailListesi:
                if email not in gorevliEmailListesi:
                    raise Exception(f"{email} görevli kullanıcılar arasında değil!")

            if user.email not in emailListesi:
                emailListesi.append(user.email)

        else:
            emailListesi = [user.email]

        rapor_obj = RaporModel(
            baslik = input.baslik,
            aciklama = input.aciklama,
            raporOlusturan = user,
            raporDuzenleyen = user,
            raporRevize = revize,
        )
        rapor_obj.save()

        kullanici_queryset = UserModel.objects.filter(email__in=emailListesi)
        rapor_obj.raporKullanicilar.set(kullanici_queryset)

        if input.raporDosya:
            raporDosyalar =DosyaEkModel.objects.filter(id__in=input.raporDosya)

            rapor_obj.raporDosya.set(raporDosyalar)
     
        if input.raporResim:
            raporResimler =GorselEkModel.objects.filter(id__in=input.raporResim)

            rapor_obj.raporResim.set(raporResimler)

        raporYazanKullanicilar = set(
            email.lower() for email in RaporModel.objects.filter(
                raporRevize=revize
            ).prefetch_related("raporKullanicilar")
            .values_list("raporKullanicilar__email", flat=True)
        )

        gorevlilerQs = revize.revizeKullanicilar.all()

        gorevliKullanicilar = set(
            gorevlilerQs.values_list("email",flat =True)
        )

        raporYazanKullanicilar = set(email.lower() for email in raporYazanKullanicilar)
        gorevliKullanicilar = set(email.lower() for email in gorevliKullanicilar)

        if raporYazanKullanicilar == gorevliKullanicilar:
            revize.revizeDurumu = 'revizeOnayBekleniyor'
            revize.save()

            revize.gorev.gorevDurumu = 'gorevOnayBekleniyor'
            revize.gorev.save()

        return rapor_obj
    
    @strawberry.mutation
    def revizeOnayla(self, info:Info, revize_id:int) -> str:
        request = info.context["request"]
        user = getAuthenticatedUser(request)
        if not user.is_authenticated:
            raise Exception("Giriş yapmış olmalısınız.")
        
        if user.userType != "yönetici":
            raise Exception("Bu işlem için yönetici olmasınız.")
        
        revize = RevizeModel.objects.get(id=revize_id)

        revize.revizeDurumu = 'revizeOnaylandi'
        revize.save()

        return "Revize ve Görev durumu onaylandı olarak değişti."
    
    @strawberry.mutation
    def revizeIptal(self,info:Info,revize_id:int) -> str:
        request = info.context["request"]
        user = getAuthenticatedUser(request)
        if not user.is_authenticated:
            raise Exception("Giriş yapmış olmalısınız.")
        
        if user.userType != "yönetici":
            raise Exception("Bu işlem için yönetici olmasınız.")
        
        revize = RevizeModel.objects.get(id=revize_id)

        revize.revizeDurumu = 'revizeIptal'
        revize.save()

        return "Revize ve Görev durumu iptal olarak değişti."

        #signal ile oto görev durumu değişti


    
    #görev üstünde onay iptal durumunu elle yapmak istersen

    # @strawberry.mutation 
    # def gorevOnayla(self, info:Info, gorev_id:int) -> str:
    #     request = info.context["request"]
    #     user = getAuthenticatedUser(request)
    #     if not user.is_authenticated:
    #         raise Exception("Giriş yapmış olmalısınız.")
        
    #     if user.userType != "yönetici":
    #         raise Exception("Bu işlem için yönetici olmalısınız!")

    #     gorev = GorevModel.objects.get(id=gorev_id)

    #     gorev.gorevDurumu = "onaylandı"
    #     gorev.save()

    #     return f"Görev (ID: {gorev.id}) başarıyla onaylandı"
    
    # @strawberry.mutation
    # def gorevIptalEt(self,info:Info,gorev_id:int) -> str:
    #     request = info.context["request"]
    #     user = getAuthenticatedUser(request)
    #     if not user.is_authenticated:
    #         raise Exception("Giriş yapmış olmalısınız.")
        
    #     if user.userType != "yönetici":
    #         raise Exception("Bu işlem için yönetici olmalısınız!")
        
    #     gorev = GorevModel.objects.get(id=gorev_id)

    #     gorev.gorevDurumu = "iptal"
    #     gorev.save()

    #     RevizeModel.objects.filter(gorev=gorev).update(aktif=False)()

    #     return f"Görev (ID: {gorev.id}) iptal edildi"
    
    @strawberry.mutation
    def revizeGuncelleme(
        self,
        info:Info,
        oncekiRevizeId:int,
        baslik:str,
        aciklama:str,
        kullaniciEmailListesi: List[str]

    )-> RevizeType:
        request = info.context["request"]
        user = getAuthenticatedUser(request)
        if not user.is_authenticated or user.userType != "yönetici":
            raise Exception("Bir yönetici hesabına giriş yapmış olmalısınız.")
        
        try:
            oncekiRevize=RevizeModel.objects.get(id=oncekiRevizeId)
            #revize durumlarına göre yeni revize oluşturmak için
            if oncekiRevize.revizeDurumu =="revizeOnaylandi":
                raise Exception("Onaylanmış bir revizeye alt revize oluşturamazsınız")
            if oncekiRevize.revizeDurumu =="revizeIptal":
                raise Exception("İptal edilen bir revizeye alt revize oluşturamazsınız")
            if oncekiRevize.revizeDurumu =="revizeGuncellendi":
                raise Exception("Güncellenmiş bir revizeye alt revize oluşturamazsınız")            
        except RevizeModel.DoesNotExist:
            raise Exception("Önceki revize bulunamadı")
        
        

        # önceki revizede olmayan kullanıcı eklenebilsin mi? 
        
        # oncekiKullanicilar = oncekiRevize.revizeKullanicilar.values_list("email",flat=True)
        # for email in kullaniciEmailListesi:
        #     if email not in oncekiKullanicilar:
        #         raise Exception(f"{email} önceki revizede yok,eklenemez.")
        
        oncekiRevize.save()
        
        gorev = oncekiRevize.gorev

        yeniRevize = RevizeModel(
            baslik=baslik,
            aciklama=aciklama,
            gorev= gorev,
            revizeOlusturan=user,
            revizeDuzenleyen=user,
            oncekiRevize=oncekiRevize,
        )
        yeniRevize.save()

        kullanicilar = UserModel.objects.filter(email__in=kullaniciEmailListesi)
        yeniRevize.revizeKullanicilar.set(kullanicilar)

        oncekiRevize.revizeDurumu = 'revizeGuncellendi'
        oncekiRevize.revizeDuzenleyen = user
        oncekiRevize.save()

        gorev.gorevDurumu = 'gorevAtandi'
        gorev.save()

        return yeniRevize
    
    @strawberry.mutation
    def raporGuncelleme(self, info:Info, input:RaporGuncelleInput) -> RaporType:
        request = info.context["request"]
        user = getAuthenticatedUser(request)
        print('user', user)
        try:
            with transaction.atomic():
                rapor = RaporModel.objects.get(id=input.id,raporKullanicilar=user)


                if input.baslik is not None:
                    rapor.baslik=input.baslik
                if input.aciklama is not None:
                    rapor.aciklama=input.aciklama
                rapor.raporDuzenlemeTarihi = datetime.datetime.now()
                rapor.raporDuzenleyen = user
                
                rapor.save()

                if input.raporDosyaId is not None:
                    rapor.raporDosya.set(DosyaEkModel.objects.filter(id__in=input.raporDosyaId))
                if input.raporResimId is not None:
                    rapor.raporResim.set(GorselEkModel.objects.filter(id__in=input.raporResimId))

                return rapor
        except RaporModel.DoesNotExist:
            raise Exception("rapor bulunamadı")
    

    # Onesignal bildirimi
    @strawberry.mutation
    def testBildirimi(self, message: str) -> bool:
        return sendOnesignalMessages(message)
schema = strawberry.Schema(query=Query,
mutation=Mutation,
subscription=Subscription)