# Görevlendirme ve Gerçek Zamanlı Bildirim Sistemi
Bu proje, yöneticilerin çalışanlara görev atayabildiği, görev durumlarının takip edilebildiği ve GraphQL tabanlı bir API üzerine inşa edilmiş modern bir görev yönetim sistemidir. Sistem, WebSocket üzerinden anlık (real-time) tarayıcı bildirimleri ve OneSignal entegrasyonu ile push bildirimleri sunarak kesintisiz bir iletişim sağlar.

# Öne Çıkan Özellikler
Modern API Mimarisi: İstemci ve sunucu arasındaki veri akışı Strawberry GraphQL kullanılarak optimize edilmiştir.

Gerçek Zamanlı Bildirimler (WebSockets): Yeni bir görev atandığında, ilgili kullanıcıya sayfa yenilenmeden Django Channels ve ASGI mimarisi kullanılarak anlık bildirim (Toast ve Masaüstü Bildirimi) gönderilir.

Push Notifications: Güvenli arka plan işlemleriyle entegre edilmiş OneSignal sayesinde kullanıcılara doğrudan sistem bildirimleri fırlatılabilir.

Güvenli Kimlik Doğrulama: REST istekleri ve WebSocket bağlantılarında güvenliği sağlamak için Django Rest Knox ile Token tabanlı (Token Authentication) doğrulama kullanılmıştır.

Gelişmiş Görev Yönetimi: Görev atama, durum güncelleme (Görev Atandı, Onay Bekleniyor vb.), çoklu görevli ataması ve dosya/görsel eki desteği.

# Kullanılan Teknolojiler
Python 3.x

Django

Strawberry GraphQL (Django Entegrasyonu)

Django Channels & Redis / InMemory (WebSocket için)

Django Rest Knox (Authentication)

SQLite (Geliştirme aşaması için)

# Projeden Elde Edilen Kazanımlar
Bu proje, bir backend geliştirme sürecinin uçtan uca nasıl planlanıp hayata geçirileceğini öğrenmek adına temel bir basamak olmuştur. Geliştirme süreci boyunca elde edilen temel teknik ve mimari yetkinlikler şunlardır:

Modern API Tasarımı: Klasik REST mimarisinin ötesine geçilerek, GraphQL (Strawberry) ile istemcinin sadece ihtiyacı olan veriyi çektiği, esnek ve tip güvenli (type-safe) bir API mimarisi kurgulanmıştır. Query ve Mutation yapıları detaylıca öğrenilmiştir.

Asenkron İletişim ve Gerçek Zamanlı Veri (Real-Time): Klasik istek-cevap (request-response) döngüsünün dışına çıkılarak, Django Channels ve WebSockets ile asenkron (ASGI) veri iletimi, kullanıcıya anlık bildirim fırlatma ve kanal/grup (channel layers) mantığı kavranmıştır.

Güvenlik ve Kimlik Doğrulama:

Kullanıcı oturumları Knox Token Authentication ile güvenli hale getirilmiş, WebSocket bağlantılarında custom middleware yazılarak token doğrulaması yapılmıştır.

Üçüncü parti servislerin (OneSignal) gizli API anahtarları .env dosyalarıyla izole edilmiş ve API şemalarından gizlenerek veri sızıntısı (data leak) prensiplerine uygun hareket edilmiştir.

Versiyon Kontrol Sistemleri (Git): Projenin versiyonlanması sürecinde git komutları, .gitignore yapısının doğru kurgulanması, hassas/gereksiz dosyaların (veritabanı, pycache, venv) depodan izole edilmesi ve temiz bir "commit" geçmişi oluşturma alışkanlığı kazanılmıştır.

Hata Ayıklama (Debugging) ve Çözüm Üretme: Frontend ve backend arasındaki veri uyuşmazlıkları, asenkron veritabanı sorgu hataları (database_sync_to_async) ve model ilişkileri (ManyToManyField vb.) üzerindeki karmaşık senaryolar başarılı bir şekilde çözümlenmiştir.
