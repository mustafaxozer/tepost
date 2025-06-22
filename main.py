# -*- coding: utf-8 -*-

from telethon import TelegramClient, events
from datetime import datetime, date, time
import asyncio

# Telegram API bilgilerin (my.telegram.org'dan al)
api_id =  20334924 # <-- BURAYA KENDİ api_id'ni yaz
api_hash = 'd26005ad572e6e501970ec53312ef82f'  # <-- BURAYA KENDİ api_hash'ini yaz

# Oturum adı
client = TelegramClient('mustafa_session', api_id, api_hash)

# Kaynak grup (dinlenecek olan)
SOURCE_GROUP = 'dostlar_mekan'

# İlk 5 fotoğraf için özel hedef gruplar
TARGETS_BY_INDEX = {
    1: ['teorikeslesme1', 'borsaanketleri', 'megaphissesii'],
    2: ['teorikeslesme2', 'analisthedefleri', 'sdttrhissesi'],
    3: ['teorikeslesme3', 'ekonomikitaplari', 'tarihtebuguntur'],
    4: ['teorikeslesme4', 'tavandabekleyenlot', 'gunicihaberler'],
    5: ['teorikeslesme4', 'tavandabekleyenlot', 'gunicihaberler'],
}

# 6. ve sonrası için tüm gruplar
ALL_GROUPS = list(set(
    sum(TARGETS_BY_INDEX.values(), [])
))

# Sayaç ve gün bilgisi
photo_counter = 0
current_day = date.today()

# Saat aralığı kontrolü (09:39–09:59)
def is_within_time_window():
    now = datetime.now().time()
    return time(9, 39) <= now <= time(9, 59)

# Hafta içi kontrolü (Pazartesi–Cuma)
def is_weekday():
    return datetime.today().weekday() < 5  # 0 = Pazartesi, 4 = Cuma

# Ana event handler
@client.on(events.NewMessage(chats=SOURCE_GROUP))
async def handler(event):
    global photo_counter, current_day

    # Zaman kontrolü
    if not is_weekday() or not is_within_time_window():
        return

    # Fotoğraf veya medya kontrolü
    if not event.photo and not event.file:
        return

    # Gün değişmişse sayaç sıfırla
    if current_day != date.today():
        photo_counter = 0
        current_day = date.today()

    photo_counter += 1
    print(f"[{datetime.now()}] 📷 {photo_counter}. fotoğraf geldi.")

    # Hedef grupları belirle
    targets = TARGETS_BY_INDEX.get(photo_counter, ALL_GROUPS)

    # Fotoğrafı hedef gruplara gönder
    for group in targets:
        try:
            await client.send_file(f'@{group}', event.media, caption=event.text or "")
            print(f"✅ Gönderildi → @{group}")
            await asyncio.sleep(1)  # spam koruması
        except Exception as e:
            print(f"❌ HATA (@{group}): {e}")

# Uygulamayı başlat
client.start()
print("🚀 Dinleme başladı... Fotoğraflar izleniyor.")
client.run_until_disconnected()
