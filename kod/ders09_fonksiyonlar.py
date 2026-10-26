# =============================================================================
# Python Kursu — Ders 9 (Hafta 5, Gün 1)
# Konu: Fonksiyonlar (def, parametre, return, varsayılan değer, kapsam) ve try/except
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
#   - Her hücre kendi fonksiyonunu tanımlar; hücreler bağımsız çalışır.
#   - input() içeren hücreler klavyeden giriş bekler.
# =============================================================================


# %% Ödev kontrolü — Ders 8 Ödev 1: sınıf raporu (kısaltılmış harf ölçeği)
ogrenciler = ["Ayşe", "Can", "Ece"]
notlar = [88, 45, 72]
for ad, puan in zip(ogrenciler, notlar):
    if puan >= 85:
        harf = "BA+"
    elif puan >= 60:
        harf = "CC–BB"
    else:
        harf = "FF–FD"
    print(f"{ad:<6}{puan:>4}  {harf}")


# %% Bölüm 1 — İlk fonksiyon: def ve çağırma
def selamla():
    print("Merhaba!")
    print("Kursa hoş geldiniz.")

selamla()
selamla()


# %% Bölüm 2 — Parametreler
def selamla(ad):
    print(f"Merhaba {ad}!")

def kdv_goster(fiyat, oran):
    print(f"{fiyat} TL + %{oran} KDV = {fiyat * (1 + oran / 100):.2f} TL")

selamla("Ayşe")
selamla("Mehmet")
kdv_goster(100, 20)
kdv_goster(250, 10)


# %% Bölüm 3 — return: sonucu geri vermek
def kdv_ekle(fiyat, oran):
    return fiyat * (1 + oran / 100)

kitap = kdv_ekle(100, 10)
kahve = kdv_ekle(85, 20)
print(f"Kitap: {kitap:.2f} TL")
print(f"Toplam: {kitap + kahve:.2f} TL")
print(f"{kdv_ekle(1000, 20):.2f}")


# %% Bölüm 4a — print eden fonksiyon None döndürür
def kare_yaz(x):
    print(x * x)

sonuc = kare_yaz(4)
print("Sonuç:", sonuc)


# %% Bölüm 4b — return eden fonksiyon
def kare(x):
    return x * x

sonuc = kare(4)
print("Sonuç:", sonuc)


# %% Bölüm 5 — Erken return ve birden fazla değer döndürmek
def harf_notu(puan):
    if puan >= 85:
        return "BA"
    if puan >= 70:
        return "CC"
    if puan >= 50:
        return "FD"
    return "FF"

def istatistik(sayilar):
    return min(sayilar), max(sayilar), sum(sayilar) / len(sayilar)

print(harf_notu(92), harf_notu(73), harf_notu(30))
en_kucuk, en_buyuk, ort = istatistik([70, 85, 92])
print(en_kucuk, en_buyuk, round(ort, 1))


# %% Bölüm 6 — Varsayılan değerler ve isimli argümanlar
def fiyat_hesapla(tutar, kdv=20, indirim=0):
    indirimli = tutar * (1 - indirim / 100)
    return round(indirimli * (1 + kdv / 100), 2)

print(fiyat_hesapla(100))
print(fiyat_hesapla(100, 10))
print(fiyat_hesapla(100, indirim=15))
print(fiyat_hesapla(indirim=15, tutar=100, kdv=1))


# %% Bölüm 7 — Belge metni (docstring)
def vki(kilo, boy):
    """Kilo (kg) ve boy (m) alır, vücut kitle indeksini döndürür."""
    return kilo / boy ** 2

print(round(vki(70, 1.75), 2))
print(vki.__doc__)


# %% Bölüm 8 — Kapsam: yerel ve global değişkenler
sepet_toplam = 0

def ekle(fiyat):
    adet = 1
    return sepet_toplam + fiyat * adet

print(ekle(50))
print(sepet_toplam)
# print(adet)  # NameError: name 'adet' is not defined


# %% Bölüm 9 — Global değeri değiştirmek: parametre + return
sayac = 0

def artir(deger):
    return deger + 1

sayac = artir(sayac)
sayac = artir(sayac)
print(sayac)


# %% Bölüm 10 — try/except: hatayı yakalamak
giris = input("Bir sayı girin: ")
try:
    sayi = int(giris)
    print("Karesi:", sayi ** 2)
except ValueError:
    print(f"'{giris}' bir sayı değil.")
print("Program devam ediyor.")


# %% Bölüm 11 — Birden fazla except, else ve finally
def bol(a, b):
    try:
        sonuc = a / b
    except ZeroDivisionError:
        print("Sıfıra bölünemez.")
        return None
    except TypeError:
        print("Yalnızca sayılar bölünebilir.")
        return None
    else:
        return round(sonuc, 2)
    finally:
        print("bol() bitti.")

print(bol(10, 3))
print(bol(10, 0))
print(bol("10", 2))


# %% Bölüm 12 — Güvenli giriş fonksiyonu: while + try/except + return
def sayi_al(mesaj, en_az=None, en_cok=None):
    while True:
        giris = input(mesaj).strip().replace(",", ".")
        try:
            sayi = float(giris)
        except ValueError:
            print("Lütfen bir sayı yazın.")
            continue
        if en_az is not None and sayi < en_az:
            print(f"En az {en_az} olmalı.")
        elif en_cok is not None and sayi > en_cok:
            print(f"En çok {en_cok} olabilir.")
        else:
            return sayi

puan = sayi_al("Not (0-100): ", 0, 100)
print("Kaydedildi:", puan)


# %% Bölüm 13a — Tuzak: çıplak except yazım hatasını gizler
notlar = [70, 80]
try:
    ortalama = sum(notlar) / len(notlar)
    print("Ortalama:", ortalma)
except:
    print("Bir şeyler ters gitti.")


# %% Bölüm 13b — Doğrusu: yalnızca beklenen hatayı yakala
notlar = []
try:
    ortalama = sum(notlar) / len(notlar)
    print("Ortalama:", ortalama)
except ZeroDivisionError:
    print("Hiç not girilmemiş.")


# %% Uygulama 1 — Fiyat hesaplama fonksiyonları
def indirim_uygula(tutar, oran=0):
    """Tutara yüzde indirim uygular."""
    return tutar * (1 - oran / 100)

def kdv_ekle(tutar, kdv=20):
    """Tutara KDV ekler."""
    return tutar * (1 + kdv / 100)

def taksit_hesapla(tutar, taksit=1):
    """Toplamı eşit taksitlere böler."""
    return tutar / taksit

def tl(tutar):
    """Sayıyı Türk lirası biçiminde metne çevirir: 1.234,50 TL"""
    metin = f"{tutar:,.2f}"
    return metin.replace(",", "X").replace(".", ",").replace("X", ".") + " TL"

liste_fiyati = 12500
indirimli = indirim_uygula(liste_fiyati, 15)
toplam = kdv_ekle(indirimli)
aylik = taksit_hesapla(toplam, 6)
print("Liste fiyatı :", tl(liste_fiyati))
print("İndirimli    :", tl(indirimli))
print("KDV dahil    :", tl(toplam))
print("6 taksit     :", tl(aylik), "/ ay")


# %% Uygulama 2 — Metin temizleme fonksiyonları (Türkçe büyük-küçük harf)
def tr_buyuk(metin):
    """Türkçe kurallarıyla büyük harf: i → İ, ı → I."""
    return metin.replace("i", "İ").replace("ı", "I").upper()

def tr_kucuk(metin):
    """Türkçe kurallarıyla küçük harf: I → ı, İ → i."""
    return metin.replace("I", "ı").replace("İ", "i").lower()

def ad_duzelt(ad):
    """'  İLKER   ışık ' → 'İlker Işık'"""
    kelimeler = ad.split()
    duzgun = []
    for k in kelimeler:
        duzgun.append(tr_buyuk(k[0]) + tr_kucuk(k[1:]))
    return " ".join(duzgun)

def telefon_temizle(tel):
    """Rakam dışındaki her şeyi atar: '(0532) 111-22 33' → '05321112233'"""
    rakamlar = ""
    for karakter in tel:
        if karakter.isdigit():
            rakamlar += karakter
    return rakamlar

kayitlar = [("  İLKER   ışık ", "(0532) 111-22 33"),
            ("ayşe nur YILMAZ", "+90 505 444 55 66"),
            ("IRMAK", "0542.777.88.99")]
for ad, tel in kayitlar:
    print(f"{ad_duzelt(ad):<16} {telefon_temizle(tel)}")


# %% Alıştırma 1 — çözüm
def dikdortgen(en, boy):
    alan = en * boy
    cevre = 2 * (en + boy)
    return alan, cevre

alan, cevre = dikdortgen(5, 3)
print(f"Alan {alan}, Çevre {cevre}")


# %% Alıştırma 2 — çözüm
def kelime_say(metin, en_az=1):
    sayac = 0
    for k in metin.split():
        if len(k) >= en_az:
            sayac += 1
    return sayac

print(kelime_say("bugün hava çok güzel"))
print(kelime_say("bugün hava çok güzel", 4))


# %% Alıştırma 3 — çözüm (düzeltilmiş)
def ortalama(sayilar):
    if not sayilar:
        return 0
    return sum(sayilar) / len(sayilar)

sonuc = ortalama([70, 80, 90])
print("Ortalama:", sonuc + 1)


# %% Alıştırma 4 — çözüm
def hesapla(a, b, islem):
    if islem == "+":
        return a + b
    elif islem == "-":
        return a - b
    elif islem == "*":
        return a * b
    elif islem == "/":
        try:
            return a / b
        except ZeroDivisionError:
            return None
    return None

print(hesapla(8, 2, "/"), hesapla(8, 0, "/"), hesapla(8, 2, "%"))


# %% Ek — Gelecek dersin önizlemesi: random modülü
import random
zar = random.randint(1, 6)
print("Zar:", zar)
