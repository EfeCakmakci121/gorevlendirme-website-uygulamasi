from strawberry.channels import GraphQLWSConsumer
import strawberry
from strawberry.types import Info
from django.contrib.auth.models import AnonymousUser
import json
from channels.generic.websocket import AsyncWebsocketConsumer

async def get_context(request, ws):
    # ws geldiğinde kullanıcı scope üzerinden alınır
    user = ws.scope.get("user", AnonymousUser())
    return {
        "request": request,
        "ws": ws,
        "user": user,
    }

class MyGraphQLWSConsumer(GraphQLWSConsumer):
    async def get_context(self, connection_params, request):
        return await get_context(request=None, ws=self)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Kullanıcının giriş yapıp yapmadığını kontrol et
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            # Kullanıcıya özel benzersiz bir grup adı oluştur (Örn: user_5)
            self.group_name = f"user_{self.scope['user'].id}"
            
            # Kullanıcıyı gruba ekle
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Bağlantı koptuğunda gruptan çıkar
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    # Gruptan gelen mesajları frontend'e ileten fonksiyon
    async def send_notification(self, event):
        message = event['message']
        # Frontend'e JSON olarak gönder
        await self.send(text_data=json.dumps({
            'type': 'new_task',
            'message': message
        }))