# =============================================================================
# Python Kursu — Ders 2 (Hafta 1, Gün 2)
# Konu: Değişkenler, Veri Tipleri (int, float, str, bool), Tip Dönüşümü, input()
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - DİKKAT: input() içeren hücreler (Bölüm 9, Uygulama 2, Alıştırma 4)
#     sizden klavyeden bir değer bekler. Hücre ile çalıştırırken giriş kutusu
#     VS Code penceresinin ÜSTÜNDE açılır; dosyanın tamamını ▶ ile
#     çalıştırırsanız terminale yazmanız gerekir.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
# =============================================================================


# %% Bölüm 1 — Değişken oluşturma (atama)
# "=" işareti: sağdaki değeri, soldaki isme ata.
urun = "Türk kahvesi"
fiyat = 85
adet = 2

print(urun)
print(fiyat * adet)
print(urun, "toplamı:", fiyat * adet, "TL")


# %% Bölüm 1b — Yeni atama yapınca isim yeni değere geçer
fiyat = 85
print(fiyat)      # 85
fiyat = 90
print(fiyat)      # 90  -> eski değer (85) artık bu isme bağlı değil

# Ders 1'deki kahve fişi sorununun çözümü: fiyatı bir kez yaz, her yerde kullan
kahve_fiyati = 85
kahve_adedi = 2
print(kahve_fiyati * kahve_adedi)   # 170


# %% Bölüm 2 — Değişken adlandırma
# Geçerli ve önerilen adlar: küçük harf, kelimeler arasında alt çizgi (snake_case)
musteri_adi = "Ayşe"
toplam_tutar = 170
kdv_orani = 0.20
urun2 = "Simit"          # rakam olabilir ama başta olamaz

# Büyük-küçük harf farklıdır: bunlar İKİ ayrı değişkendir
adet = 3
Adet = 5
print(adet, Adet)

# Geçersiz adlar (hata verdikleri için yorum satırı olarak duruyor):
#   2urun = "Simit"        -> SyntaxError: invalid decimal literal
#   musteri adi = "Ayşe"   -> SyntaxError: invalid syntax
#   fiyat-kdv = 10         -> SyntaxError: cannot assign to expression here.
#                             Maybe you meant '==' instead of '='?
#   class = 5              -> SyntaxError: invalid syntax  (class Python'un kelimesi)


# %% Bölüm 3 — Değeri güncellemek
puan = 10
print("Başlangıç:", puan)

puan = puan + 5          # sağ taraf önce hesaplanır: 10 + 5 = 15
print("Sonra:", puan)

# Kısayollar: += -= *= /=
sayac = 10
sayac += 5     # sayac = sayac + 5  -> 15
sayac -= 3     # sayac = sayac - 3  -> 12
sayac *= 2     # sayac = sayac * 2  -> 24
sayac /= 4     # sayac = sayac / 4  -> 6.0
print("Sayaç:", sayac)


# %% Bölüm 4 — Sayılar: int ve float
ogrenci_sayisi = 18          # int: tam sayı
ortalama_not = 78.5          # float: ondalıklı sayı (ayırıcı NOKTA)
butce = 1_250_000            # alt çizgi okunurluk içindir, değeri değiştirmez

print(type(ogrenci_sayisi))  # <class 'int'>
print(type(ortalama_not))    # <class 'float'>
print(butce + 1)             # 1250001
print(10 / 5)                # 2.0  -> "/" her zaman float verir
print(ogrenci_sayisi + 2.5)  # 20.5 -> int + float = float
print(0.1 + 0.2)             # 0.30000000000000004 -> ondalık sayılarda küçük farklar olur


# %% Bölüm 5 — Metinler: str
ad = "Ayşe"
soyad = 'Yılmaz'             # tek tırnak da olur, başı ve sonu aynı olmalı
tam_ad = ad + " " + soyad    # + metinleri uç uca ekler
cizgi = "-" * 20             # * metni tekrarlar

print(tam_ad)
print(cizgi)
print("5" + "5")             # 55  -> metin birleştirme, toplama değil!
print(5 + 5)                 # 10
print(type(tam_ad))          # <class 'str'>


# %% Bölüm 5b — Metin hataları (düzeltilmiş halleri)
# Hatalı halleri:
#   print("Yaş: " + 30)        -> TypeError: can only concatenate str (not "int") to str
#   mesaj = 'Python'un gücü'   -> SyntaxError: unterminated string literal (detected at line 1)
#   print("5" * "3")           -> TypeError: can't multiply sequence by non-int of type 'str'
print("Yaş: " + str(30))
mesaj = "Python'un gücü"
print(mesaj)
print("5" * 3)               # 555


# %% Bölüm 6 — Mantıksal değerler: bool ve karşılaştırma
indirimli_mi = True          # büyük harfle: True / False
stokta_var = False
print(type(indirimli_mi))    # <class 'bool'>

yas = 20
print(yas >= 18)             # True
print(yas == 20)             # True   (== karşılaştırır, = atar!)
print(yas != 20)             # False
print(yas < 10)              # False

ehliyet_alabilir = yas >= 18     # karşılaştırmanın sonucu bir değişkene konabilir
print("Ehliyet alabilir mi?", ehliyet_alabilir)


# %% Bölüm 7 — Tip dönüşümü
metin_sayi = "25"
print(int(metin_sayi) + 5)       # 30   -> str'den int'e
print(float("3.5") * 2)          # 7.0  -> str'den float'a
print(str(25) + " TL")           # 25 TL -> int'ten str'ye
print(int(3.99))                 # 3    -> int() yuvarlamaz, kesirli kısmı atar!
print(float(7))                  # 7.0
print(bool(0), bool(1))          # False True
print(bool(""), bool("Merhaba")) # False True


# %% Bölüm 8 — Tip dönüşümünde sık hatalar (düzeltilmiş halleri)
# Hata 1: Ondalıklı metni int'e çevirmek
#   int("3.5")    -> ValueError: invalid literal for int() with base 10: '3.5'
print(float("3.5"))

# Hata 2: Türkçe ondalık virgülü
#   float("3,5")  -> ValueError: could not convert string to float: '3,5'
print(float("3.5"))

# Hata 3: Sayıya çevrilemeyen metin
#   int("yirmi")  -> ValueError: invalid literal for int() with base 10: 'yirmi'
print(int("20"))

# Hata 4: Metin ile sayıyı + ile birleştirmek
#   print("Yaş: " + 30) -> TypeError: can only concatenate str (not "int") to str
print("Yaş: " + str(30))
print("Yaş:", 30)

# Hata 5 (sessiz hata!): Kodda ondalık virgül kullanmak
fiyat_hatali = 3,5
print(fiyat_hatali, type(fiyat_hatali))   # (3, 5) <class 'tuple'> -> sayı DEĞİL
fiyat_dogru = 3.5
print(fiyat_dogru, type(fiyat_dogru))     # 3.5 <class 'float'>

# Hata 6 (sessiz hata!): Binlik ayırıcı olarak nokta kullanmak
butce_hatali = 1.000
print(butce_hatali)                       # 1.0 -> bin değil, BİR!
butce_dogru = 1_000
print(butce_dogru)                        # 1000
#   butce = 1.000.000  -> SyntaxError: invalid syntax


# %% Bölüm 9 — input(): kullanıcıdan bilgi almak  [GİRİŞ BEKLER]
ad = input("Adınız: ")
print("Merhaba", ad)

yas_metin = input("Yaşınız: ")
print(type(yas_metin))               # <class 'str'> -> input HER ZAMAN str döndürür

yas = int(yas_metin)                 # hesap yapmak için sayıya çeviriyoruz
print("Gelecek yıl", yas + 1, "yaşında olacaksınız.")


# %% Bölüm 10 — Uygulama 1: Market sepeti (değişkenlerle)
ekmek_fiyati = 15
sut_fiyati = 38.5
yumurta_fiyati = 95.75

ekmek_adedi = 2
sut_adedi = 3
yumurta_adedi = 1

toplam = ekmek_fiyati * ekmek_adedi + sut_fiyati * sut_adedi + yumurta_fiyati * yumurta_adedi
indirim_orani = 0.10
indirim = toplam * indirim_orani
odenecek = toplam - indirim

print("Toplam:", toplam, "TL")
print("İndirim:", indirim, "TL")
print("Ödenecek:", odenecek, "TL")


# %% Bölüm 11 — Uygulama 2: Yaş hesaplayıcı  [GİRİŞ BEKLER]
bu_yil = 2026
dogum_yili = int(input("Doğum yılınız: "))

yas = bu_yil - dogum_yili
gun = yas * 365
resit_mi = yas >= 18

print("Yaşınız (yaklaşık):", yas)
print("Yaklaşık gün:", gun)
print("18 yaşından büyük mü?", resit_mi)


# =============================================================================
# SINIF İÇİ ALIŞTIRMALARIN ÇÖZÜMLERİ
# =============================================================================

# %% Alıştırma 1 (kolay) — Kendinizi değişkenlerle tanıtın
ad = "Ayşe"
yas = 30
boy = 1.65
ogrenci_mi = True

print(ad, yas, boy, ogrenci_mi)
print(type(ad), type(yas), type(boy), type(ogrenci_mi))


# %% Alıştırma 2 (kolay-orta) — Oda için parke hesabı
uzunluk = 5
genislik = 3.5
parke_m2_fiyati = 350

alan = uzunluk * genislik
cevre = 2 * (uzunluk + genislik)
maliyet = alan * parke_m2_fiyati

print("Alan:", alan, "m²")
print("Çevre:", cevre, "m")
print("Parke maliyeti:", maliyet, "TL")


# %% Alıştırma 3 (orta) — Hata avı (düzeltilmiş hali)
# Hatalı hali:
#   Ad = "Zeynep"
#   dogum yili = 1995
#   yas = 2026 - dogum_yili
#   print("Merhaba " + ad + ", yaşın: " + yas)
ad = "Zeynep"
dogum_yili = 1995
yas = 2026 - dogum_yili
print("Merhaba " + ad + ", yaşın: " + str(yas))


# %% Alıştırma 4 (zor) — Sıcaklık dönüştürücü  [GİRİŞ BEKLER]
celsius = float(input("Sıcaklık (°C): "))

fahrenheit = celsius * 9 / 5 + 32
kelvin = celsius + 273.15
donma_altinda_mi = celsius < 0

print("Fahrenheit:", fahrenheit)
print("Kelvin:", kelvin)
print("Donma noktasının altında mı?", donma_altinda_mi)


# %% Ek — Gelecek dersin önizlemesi: string metotları
sehir = "istanbul"
print(sehir.upper())     # ISTANBUL  -> "İ" bekliyorduk! Türkçe İ/ı tuzağı Ders 3'te.
