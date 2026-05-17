import requests
from .models import OneSignalApiModel

def sendOnesignalMessages(message: str) -> bool:
    # 1. Ayarları veritabanından çek (Güvenli yöntem)
    ayar = OneSignalApiModel.objects.first()
    
    # 2. Hata kontrolleri
    if not ayar:
        print("Sistem Hatası: OneSignal ayarları veritabanında yok.")
        return False
        
    app_id = ayar.oneSignalApiId
    api_key = ayar.oneSignalApiKey
    
    if not app_id or not api_key:
        print("Sistem Hatası: Eksik OneSignal bilgisi.")
        return False

    # 3. Headers ve Payload (Basic 'B' harfi büyük olmalı)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {api_key}", 
    }

    payload = {
        "app_id": app_id,
        "included_segments": ["All"],
        "contents": {"en": message},
    }

    # 4. İsteği Gönder ve Sonucu Döndür
    try:
        response = requests.post(
            "https://onesignal.com/api/v1/notifications",
            json=payload,
            headers=headers
        )
        # Sadece test aşamasındaysan print'leri bırakabilirsin, canlıda silinmesi tavsiye edilir.
        print("OneSignal Status Code:", response.status_code) 
        
        return response.status_code == 200
    except Exception as e:
        print(f"OneSignal Bağlantı Hatası: {e}")
        return False