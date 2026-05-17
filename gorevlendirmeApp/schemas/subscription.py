# subscriptions.py
import json
import strawberry
from typing import AsyncGenerator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def gorevCreated(self, info) -> AsyncGenerator[str, None]:
        channel_layer = get_channel_layer()
        group_name = "gorev_bildirimleri"

        # Mevcut channel'ı gruba ekle
        await channel_layer.group_add(
            group_name,
            info.context["connection_scope"]["channel_name"]
        )

        try:
            while True:
                message = await info.context["ws"].receive_json()
                yield message
        finally:
            # Bağlantı kopunca gruptan çıkar
            await channel_layer.group_discard(
                group_name,
                info.context["connection_scope"]["channel_name"]
            )
