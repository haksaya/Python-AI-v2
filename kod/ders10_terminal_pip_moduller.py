# =============================================================================
# Python Kursu — Ders 10 (Hafta 5, Gün 2)
# Konu: Terminal ve temel komutlar, pip, sanal ortam, modüller (random, datetime), PyCharm, dosya okuma/yazma
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Bu dersin Python kodları için ek kurulum GEREKMEZ (random, datetime Python ile gelir).
#   - Terminal komutları bu dosyada YORUM olarak yer alır; terminale yazılır, Python'a değil.
#   - Bölüm 7 aynı klasörde metin_araclari.py dosyasını ister (dersle birlikte verildi).
#   - Dosya hücreleri, dosyanın bulunduğu klasörde notlar.txt ve dogum_gunleri.txt oluşturur.
# =============================================================================


# %% Ödev kontrolü — Ders 9 Ödev 3: sifre_kontrol
def sifre_kontrol(sifre):
    eksikler = []
    if len(sifre) < 8:
        eksikler.append("en az 8 karakter")
    if sifre == sifre.lower():
        eksikler.append("en az bir büyük harf")
    if sifre.isalpha():
        eksikler.append("rakam ya da sembol")
    return eksikler

print(sifre_kontrol("kedi"))
print(sifre_kontrol("Python2026!"))


# %% Blok 1 — Terminal komutları (TERMİNALE yazılır; burada yalnızca yorum olarak duruyor)
# --- Gezinme ---
# pwd                      -> neredeyim?
# ls        (Windows: ls ya da dir)
# cd proje                 -> klasöre gir
# cd ..                    -> bir üst klasöre çık
# mkdir ornekler           -> klasör oluştur
# cls / clear              -> ekranı temizle
#
# --- Python ---
# python --version         (Windows: py --version, macOS: python3 --version)
# python merhaba.py        -> dosyayı çalıştır
# python -c "print('Selam')"
#
# --- pip ---
# python -m pip install requests
# python -m pip list
# python -m pip show requests
# python -m pip uninstall requests
#
# --- Sanal ortam ---
# python -m venv .venv
# .venv\Scripts\Activate.ps1        (Windows PowerShell)
# source .venv/bin/activate        (macOS / Linux)
# python -m pip freeze > requirements.txt
# python -m pip install -r requirements.txt
# deactivate


# %% Bölüm 1 — Üç import biçimi
import random
print(random.randint(1, 6))

from random import choice
print(choice(["taş", "kâğıt", "makas"]))

import datetime as dt
print(dt.date.today().year)


# %% Bölüm 2 — random modülü
import random

random.seed(42)
print(random.randint(1, 6))
print(random.random())
print(random.choice(["Ali", "Ece", "Can"]))
kartlar = ["A", "K", "Q", "J"]
random.shuffle(kartlar)
print(kartlar)
print(random.sample(range(1, 50), 6))


# %% Bölüm 3 — datetime: tarih farkı, timedelta, strftime
from datetime import date, datetime, timedelta

bugun = date(2026, 10, 26)
dogum = date(1990, 3, 15)
yas_gun = (bugun - dogum).days
print("Yaşanan gün:", yas_gun)
print("Yaş:", yas_gun // 365)
print("100 gün sonra:", bugun + timedelta(days=100))
yilbasi = date(bugun.year + 1, 1, 1)
print("Yılbaşına:", (yilbasi - bugun).days, "gün")
print(datetime(2026, 10, 26, 9, 30).strftime("%d.%m.%Y %H:%M"))


# %% Bölüm 4 — Türkçe tarih ve tam yaş
from datetime import date

AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
         "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma",
          "Cumartesi", "Pazar"]

def tr_tarih(t):
    return f"{t.day} {AYLAR[t.month - 1]} {t.year}, {GUNLER[t.weekday()]}"

def tam_yas(dogum, bugun):
    yas = bugun.year - dogum.year
    if (bugun.month, bugun.day) < (dogum.month, dogum.day):
        yas -= 1
    return yas

print(tr_tarih(date(2026, 10, 29)))
print(tam_yas(date(1990, 11, 2), date(2026, 10, 26)))


# %% Bölüm 5 — Kendi modülümüzü kullanmak (metin_araclari.py aynı klasörde olmalı)
import metin_araclari as ma

print(ma.ad_duzelt("İLKER   ışık"))
print(ma.tr_buyuk("istanbul"))


# %% Bölüm 6 — Dosyaya yazmak: w ve a modları
with open("notlar.txt", "w", encoding="utf-8") as dosya:
    dosya.write("Ayşe,88\n")
    dosya.write("Mehmet,64\n")

with open("notlar.txt", "a", encoding="utf-8") as dosya:
    dosya.write("Zeynep,95\n")

with open("notlar.txt", encoding="utf-8") as dosya:
    print(dosya.read())


# %% Bölüm 7 — Dosyayı satır satır okumak
notlar = {}
with open("notlar.txt", encoding="utf-8") as dosya:
    for satir in dosya:
        ad, puan = satir.strip().split(",")
        notlar[ad] = int(puan)
print(notlar)
print("Ortalama:", sum(notlar.values()) / len(notlar))


# %% Uygulama 1 — Zar oyunu (random + fonksiyonlar)
import random

def zar_at():
    return random.randint(1, 6), random.randint(1, 6)

def oyna(oyuncular, tur_sayisi=3):
    puanlar = {ad: 0 for ad in oyuncular}
    for tur in range(1, tur_sayisi + 1):
        for ad in oyuncular:
            z1, z2 = zar_at()
            cift = " (çift! +5)" if z1 == z2 else ""
            puanlar[ad] += z1 + z2 + (5 if cift else 0)
            print(f"Tur {tur} | {ad:<5} {z1}+{z2}{cift}")
    return puanlar

sonuc = oyna(["Ayşe", "Can"])
kazanan = max(sonuc, key=sonuc.get)
print(sonuc, "→ Kazanan:", kazanan)


# %% Uygulama 2 — Doğum günü takvimi (dosya + datetime)
from datetime import date

AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
         "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

def sonraki_dogum_gunu(dogum, bugun):
    aday = date(bugun.year, dogum.month, dogum.day)
    if aday < bugun:
        aday = date(bugun.year + 1, dogum.month, dogum.day)
    return aday

with open("dogum_gunleri.txt", "w", encoding="utf-8") as f:
    f.write("Ayşe,1990-11-02\nMehmet,1985-03-15\nZeynep,2001-10-30\n")

bugun = date(2026, 10, 26)   # gerçek kullanımda: date.today()
liste = []
with open("dogum_gunleri.txt", encoding="utf-8") as f:
    for satir in f:
        ad, tarih = satir.strip().split(",")
        dogum = date.fromisoformat(tarih)
        sonraki = sonraki_dogum_gunu(dogum, bugun)
        liste.append(((sonraki - bugun).days, ad, sonraki))

for kalan, ad, t in sorted(liste):
    print(f"{ad:<7} {t.day} {AYLAR[t.month - 1]:<6} → {kalan:>3} gün kaldı")


# %% Alıştırma 1 — çözüm
import random
import string
harfler = string.ascii_letters + string.digits
sifre = ""
for _ in range(8):
    sifre += random.choice(harfler)
print(sifre)


# %% Alıştırma 2 — çözüm
from datetime import date
not_ = input("Bugünün notu: ")
with open("gunluk.txt", "a", encoding="utf-8") as f:
    f.write(f"{date.today():%d.%m.%Y} - {not_}\n")
with open("gunluk.txt", encoding="utf-8") as f:
    print(f.read())


# %% Alıştırma 3 — çözüm
from datetime import date

girdi = input("Tarih (GG.AA.YYYY): ").strip()
try:
    gun, ay, yil = girdi.split(".")
    tarih = date(int(yil), int(ay), int(gun))
except ValueError:
    print("Geçersiz tarih ya da biçim.")
else:
    fark = (tarih - date.today()).days
    if fark >= 0:
        print(f"{fark} gün sonra")
    else:
        print(f"{-fark} gün önce")


# %% Ek — Gelecek dersin önizlemesi: json modülü
import json
veri = '{"ad": "Ayşe", "yas": 34}'
kisi = json.loads(veri)
print(kisi["ad"])
