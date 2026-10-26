# =============================================================================
# Python Kursu — Ders 11 (Hafta 6, Gün 1)
# Konu: JSON, XML, requests kütüphanesi, JSON ve XML ile API kullanımı (TCMB kurları, Open-Meteo)
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum (terminalde, sanal ortam etkinken): python -m pip install requests
#   - Bölüm 8 ve sonrası İNTERNET bağlantısı ister; çıktılar o günün verisine göre değişir.
#   - json ve xml.etree modülleri Python ile gelir; kurulum gerekmez.
# =============================================================================


# %% Ödev kontrolü — Ders 10 Ödev 2: harcama günlüğü (kısaltılmış, giriş yerine sabit değer)
from datetime import date
aciklama, tutar = "Market", 245.90
with open("harcamalar.txt", "a", encoding="utf-8") as f:
    f.write(f"{date.today()};{aciklama};{tutar}\n")
toplam = 0
with open("harcamalar.txt", encoding="utf-8") as f:
    for satir in f:
        toplam += float(satir.strip().split(";")[2])
print(f"Toplam harcama: {toplam:.2f} TL")


# %% Bölüm 1 — json.loads ve json.dumps
import json

metin = '{"ad": "Ayşe", "yas": 34, "ogrenci": false, "notlar": [85, 72]}'
kisi = json.loads(metin)
print(type(kisi), kisi["ad"], kisi["ogrenci"])
kisi["notlar"].append(90)
geri = json.dumps(kisi, ensure_ascii=False)
print(geri)


# %% Bölüm 1b — indent ile okunaklı JSON
import json

kisi = {"ad": "Ayşe", "yas": 34, "ogrenci": False,
        "notlar": [85, 72, 90], "telefon": None}
print(json.dumps(kisi, ensure_ascii=False, indent=2))


# %% Bölüm 2 — json.dump ve json.load ile dosyalar
import json

ayarlar = {"tema": "koyu", "dil": "tr", "yazi_boyutu": 14, "son_dosyalar": ["rapor.txt"]}
with open("ayarlar.json", "w", encoding="utf-8") as f:
    json.dump(ayarlar, f, ensure_ascii=False, indent=2)

with open("ayarlar.json", encoding="utf-8") as f:
    okunan = json.load(f)
print(okunan["tema"], okunan["yazi_boyutu"] + 2)


# %% Bölüm 3 — İç içe JSON verisini dolaşmak
import json

veri = json.loads('''{"sinif": "10-A", "ogrenciler": [
  {"ad": "Ali", "notlar": [70, 85]},
  {"ad": "Ece", "notlar": [92, 88]}]}''')
print(veri["sinif"], len(veri["ogrenciler"]), "öğrenci")
for ogr in veri["ogrenciler"]:
    ort = sum(ogr["notlar"]) / len(ogr["notlar"])
    print(f"{ogr['ad']}: {ort:.1f}")


# %% Bölüm 4a — Örnek XML dosyasını oluştur (TCMB 20.03.2018 bülteninden, kısaltılmış)
ornek = """<?xml version="1.0" encoding="UTF-8"?>
<Tarih_Date Tarih="20.03.2018" Date="03/20/2018" Bulten_No="2018/56">
  <Currency CrossOrder="0" Kod="USD" CurrencyCode="USD">
    <Unit>1</Unit>
    <Isim>ABD DOLARI</Isim>
    <CurrencyName>US DOLLAR</CurrencyName>
    <ForexBuying>3.9356</ForexBuying>
    <ForexSelling>3.9427</ForexSelling>
    <BanknoteBuying>3.9329</BanknoteBuying>
    <BanknoteSelling>3.9486</BanknoteSelling>
    <CrossRateUSD/>
    <CrossRateOther/>
  </Currency>
  <Currency CrossOrder="9" Kod="EUR" CurrencyCode="EUR">
    <Unit>1</Unit>
    <Isim>EURO</Isim>
    <CurrencyName>EURO</CurrencyName>
    <ForexBuying>4.8516</ForexBuying>
    <ForexSelling>4.8604</ForexSelling>
    <BanknoteBuying>4.8482</BanknoteBuying>
    <BanknoteSelling>4.8677</BanknoteSelling>
    <CrossRateUSD/>
    <CrossRateOther>1.2327</CrossRateOther>
  </Currency>
</Tarih_Date>"""

with open("kurlar_ornek.xml", "w", encoding="utf-8") as f:
    f.write(ornek)
print("kurlar_ornek.xml oluşturuldu.")


# %% Bölüm 4b — ElementTree ile XML okumak
import xml.etree.ElementTree as ET

kok = ET.parse("kurlar_ornek.xml").getroot()
print("Bülten tarihi:", kok.get("Tarih"))
for doviz in kok.findall("Currency"):
    kod = doviz.get("Kod")
    isim = doviz.find("Isim").text
    satis = float(doviz.find("ForexSelling").text)
    print(f"{kod} {isim:<11} {satis:.4f} TL")


# %% Bölüm 5 — requests.get ile ilk istek (internet gerekir)
import requests

url = "https://api.open-meteo.com/v1/forecast"
parametreler = {"latitude": 41.01, "longitude": 28.98, "current": "temperature_2m"}
yanit = requests.get(url, params=parametreler, timeout=10)
print("Durum kodu:", yanit.status_code)
veri = yanit.json()
print("Sıcaklık:", veri["current"]["temperature_2m"], "°C")
print(yanit.url)


# %% Bölüm 6 — Ağ hatalarını yakalamak
import requests

def veri_getir(url, **parametreler):
    try:
        yanit = requests.get(url, params=parametreler, timeout=10)
        yanit.raise_for_status()
        return yanit.json()
    except requests.exceptions.HTTPError:
        print("Sunucu hata kodu döndürdü:", yanit.status_code)
    except requests.exceptions.ConnectionError:
        print("Bağlantı kurulamadı.")
    except requests.exceptions.Timeout:
        print("Sunucu zamanında yanıt vermedi.")
    return None

print(veri_getir("https://api.open-meteo.com/v1/olmayan_uc_nokta"))
print(veri_getir("https://bu-adres-yok-12345.com"))


# %% Uygulama 1 — TCMB günlük döviz kurları (XML API, internet gerekir)
import requests
import xml.etree.ElementTree as ET

TCMB_URL = "https://www.tcmb.gov.tr/kurlar/today.xml"

def tcmb_kurlari():
    """TCMB'nin bugünkü kurlarını {kod: (isim, döviz satış)} sözlüğü olarak döndürür."""
    yanit = requests.get(TCMB_URL, timeout=10)
    yanit.raise_for_status()
    kok = ET.fromstring(yanit.content)
    kurlar = {}
    for doviz in kok.findall("Currency"):
        kod = doviz.get("Kod")
        satis = doviz.find("ForexSelling").text
        if satis:
            birim = int(doviz.find("Unit").text)
            isim = doviz.find("Isim").text
            kurlar[kod] = (isim, float(satis) / birim)
    return kok.get("Tarih"), kurlar

tarih, kurlar = tcmb_kurlari()
print(f"Bülten: {tarih} ({len(kurlar)} döviz)")
for kod in ["USD", "EUR"]:
    isim, kur = kurlar[kod]
    print(f"{kod} ({isim}): {kur:.4f} TL")
miktar = 250
print(f"{miktar} USD = {miktar * kurlar['USD'][1]:,.2f} TL")


# %% Uygulama 1b — Geçmiş tarihli TCMB bülteninin adresi
from datetime import date

def bulten_adresi(tarih):
    return f"https://www.tcmb.gov.tr/kurlar/{tarih:%Y%m}/{tarih:%d%m%Y}.xml"

print(bulten_adresi(date(2018, 3, 20)))
print(bulten_adresi(date(2026, 10, 23)))


# %% Uygulama 2 — Open-Meteo hava durumu (JSON API, internet gerekir)
import requests

SEHIRLER = {"İstanbul": (41.01, 28.98), "Ankara": (39.93, 32.86), "İzmir": (38.42, 27.14)}

def hava_durumu(enlem, boylam, gun=3):
    parametreler = {
        "latitude": enlem, "longitude": boylam,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Europe/Istanbul", "forecast_days": gun,
    }
    yanit = requests.get("https://api.open-meteo.com/v1/forecast", params=parametreler, timeout=10)
    yanit.raise_for_status()
    return yanit.json()

veri = hava_durumu(*SEHIRLER["İstanbul"])
simdi = veri["current"]
print(f"İstanbul şu an: {simdi['temperature_2m']} °C")
print(f"Rüzgâr: {simdi['wind_speed_10m']} km/sa")
gunluk = veri["daily"]
for tarih, en_yuksek, en_dusuk in zip(gunluk["time"], gunluk["temperature_2m_max"], gunluk["temperature_2m_min"]):
    print(f"{tarih}: {en_dusuk:>5.1f} / {en_yuksek:>5.1f} °C")


# %% Alıştırma 1 — çözüm
import json

kitaplar = [{"ad": "Tutunamayanlar", "yazar": "Oğuz Atay", "yil": 1972},
            {"ad": "Puslu Kıtalar Atlası", "yazar": "İhsan Oktay Anar", "yil": 1995},
            {"ad": "Kafamda Bir Tuhaflık", "yazar": "Orhan Pamuk", "yil": 2014}]
with open("kitaplar.json", "w", encoding="utf-8") as f:
    json.dump(kitaplar, f, ensure_ascii=False, indent=2)
with open("kitaplar.json", encoding="utf-8") as f:
    for k in json.load(f):
        if k["yil"] > 2000:
            print(f"{k['ad']} ({k['yazar']}, {k['yil']})")


# %% Alıştırma 2 — çözüm (internet gerekir)
import requests
import xml.etree.ElementTree as ET

TCMB_URL = "https://www.tcmb.gov.tr/kurlar/today.xml"

def tcmb_kurlari():
    """TCMB'nin bugünkü kurlarını {kod: (isim, döviz satış)} sözlüğü olarak döndürür."""
    yanit = requests.get(TCMB_URL, timeout=10)
    yanit.raise_for_status()
    kok = ET.fromstring(yanit.content)
    kurlar = {}
    for doviz in kok.findall("Currency"):
        kod = doviz.get("Kod")
        satis = doviz.find("ForexSelling").text
        if satis:
            birim = int(doviz.find("Unit").text)
            isim = doviz.find("Isim").text
            kurlar[kod] = (isim, float(satis) / birim)
    return kok.get("Tarih"), kurlar

tarih, kurlar = tcmb_kurlari()
kod = input("Döviz kodu (USD, EUR…): ").strip().upper()
if kod not in kurlar:
    print("Bu döviz bültende yok.")
else:
    tl = float(input("TL tutarı: ").replace(",", "."))
    isim, kur = kurlar[kod]
    print(f"{tl:,.2f} TL ≈ {tl / kur:,.2f} {kod}")
    print(f"Kur: {kur:.4f} ({isim})")


# %% Alıştırma 3 — çözüm (internet gerekir)
import requests

SEHIRLER = {"İstanbul": (41.01, 28.98), "Ankara": (39.93, 32.86), "İzmir": (38.42, 27.14)}

def hava_durumu(enlem, boylam, gun=3):
    parametreler = {
        "latitude": enlem, "longitude": boylam,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Europe/Istanbul", "forecast_days": gun,
    }
    yanit = requests.get("https://api.open-meteo.com/v1/forecast", params=parametreler, timeout=10)
    yanit.raise_for_status()
    return yanit.json()

sicakliklar = {}
for sehir, (enlem, boylam) in SEHIRLER.items():
    try:
        veri = hava_durumu(enlem, boylam, gun=1)
        sicakliklar[sehir] = veri["current"]["temperature_2m"]
    except requests.exceptions.RequestException:
        print(f"{sehir} için veri alınamadı.")
if sicakliklar:
    en_sicak = max(sicakliklar, key=sicakliklar.get)
    for sehir, derece in sicakliklar.items():
        print(f"{sehir}: {derece} °C")
    print(f"En sıcak: {en_sicak} ({sicakliklar[en_sicak]} °C)")


# %% Ek — Gelecek dersin önizlemesi: Streamlit (streamlit run ile çalışır; burada yorum)
# import streamlit as st
#
# st.title("Merhaba Streamlit")
# ad = st.text_input("Adınız")
# st.write("Hoş geldin,", ad)
