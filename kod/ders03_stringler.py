# =============================================================================
# Python Kursu — Ders 3 (Hafta 2, Gün 1)
# Konu: String'ler: indeksleme, dilimleme, kaçış karakterleri, f-string,
#       string metotları ve Türkçe İ/ı tuzağı
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - DİKKAT: input() içeren hücreler (Uygulama 1, Alıştırma 4) klavyeden
#     giriş bekler. Hücreyle çalıştırırken giriş kutusu VS Code'un ÜSTÜNDE açılır.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
# =============================================================================


# %% Bölüm 1 — İndeksleme: metnin tek bir karakterine erişmek
kelime = "Python"

print(kelime[0])      # P   -> sayma 0'dan başlar!
print(kelime[1])      # y
print(kelime[5])      # n   -> son karakter (6 harf: 0..5)
print(kelime[-1])     # n   -> sondan birinci
print(kelime[-2])     # o   -> sondan ikinci
print(len(kelime))    # 6   -> len() metnin uzunluğu (Ders 4'te ayrıntılı)


# %% Bölüm 2 — Dilimleme: metnin bir parçasını almak  [başlangıç:bitiş:adım]
kelime = "Python"

print(kelime[0:3])    # Pyt   -> 0, 1, 2 (bitiş DAHİL DEĞİL)
print(kelime[2:])     # thon  -> 2'den sona kadar
print(kelime[:2])     # Py    -> baştan 2'ye kadar
print(kelime[1:4])    # yth
print(kelime[::2])    # Pto   -> ikişer atlayarak
print(kelime[::-1])   # nohtyP -> tersten

# Pratik örnek: tarihi parçalarına ayırmak
tarih = "2026-10-25"
yil = tarih[:4]
ay = tarih[5:7]
gun = tarih[8:]
print(gun, ay, yil, sep=".")    # 25.10.2026


# %% Bölüm 3 — Metinler değiştirilemez (immutable)
kelime = "Python"
#   kelime[0] = "J"   -> TypeError: 'str' object does not support item assignment
yeni_kelime = "J" + kelime[1:]   # yeni bir metin oluşturuyoruz
print(yeni_kelime)               # Jython
print(kelime)                    # Python (orijinal değişmedi)


# %% Bölüm 4 — Kaçış karakterleri ve çok satırlı metin
print("Merhaba\nDünya")          # \n -> yeni satır
print("Ad\tSoyad")               # \t -> sekme (tab)
print("Ona \"selam\" dedi")      # \" -> metnin içinde çift tırnak
print("C:\\Users\\ayse")         # \\ -> ters bölü işaretinin kendisi
print(r"C:\notlar\yeni")         # r"..." -> ham metin: \ özel anlam taşımaz

adres = """Atatürk Cad. No: 12
Kadıköy
İstanbul"""                      # üç tırnak: birden fazla satır
print(adres)


# %% Bölüm 5 — f-string: değişkenleri metnin içine yerleştirmek
ad = "Ayşe"
yas = 30

print("Merhaba " + ad + ", " + str(yas) + " yaşındasın.")   # eski yol: uzun
print(f"Merhaba {ad}, {yas} yaşındasın.")                    # f-string: kısa ve okunur
print(f"Gelecek yıl {yas + 1} yaşında olacaksın.")           # {} içinde işlem yapılabilir
print(f"Adının ilk harfi: {ad[0]}")                          # {} içinde indeksleme


# %% Bölüm 6 — f-string ile sayı biçimlendirme
odenecek = 217.125
ortalama = 97.88000000000001
butce = 1234567.891
oran = 0.157
sira = 7

print(f"{odenecek:.2f} TL")      # 217.12 TL  -> virgülden sonra 2 basamak
print(f"{ortalama:.2f}")         # 97.88
print(f"{butce:,.2f}")           # 1,234,567.89 -> binlik ayırıcı (İngilizce biçim)
print(f"{oran:.1%}")             # 15.7%  -> yüzde
print(f"{sira:03d}")             # 007    -> başa sıfır ekleyerek 3 basamak


# %% Bölüm 6b — Yuvarlama sürprizi: 217.125 neden 217.12?
print(f"{0.125:.2f}")    # 0.12 -> tam ortadaki değer ÇİFT basamağa yuvarlanır
print(f"{0.375:.2f}")    # 0.38
print(f"{2.675:.2f}")    # 2.67 -> 2.675 bilgisayarda 2.67499... olarak saklanır


# %% Bölüm 7 — f-string ile hizalama: sütun sütun fiş
print(f"{'Ürün':<14}{'Tutar':>10}")
print("-" * 24)
print(f"{'Türk kahvesi':<14}{170:>10.2f}")
print(f"{'Simit':<14}{30:>10.2f}")
print(f"{'Çay':<14}{75:>10.2f}")
# :<14 -> 14 karakterlik alanda SOLA yasla, :>10 -> 10 karakterlik alanda SAĞA yasla


# %% Bölüm 8 — String metotları: büyük/küçük harf
metin = "merhaba DÜNYA"

print(metin.upper())        # MERHABA DÜNYA
print(metin.lower())        # merhaba dünya
print(metin.title())        # Merhaba Dünya
print(metin.capitalize())   # Merhaba dünya
print(metin)                # merhaba DÜNYA -> orijinal değişmedi; metotlar YENİ metin döndürür


# %% Bölüm 9 — Türkçe İ/ı tuzağı ve çözümü
print("istanbul".upper())   # ISTANBUL  (beklenen: İSTANBUL)
print("IŞIK".lower())       # işik      (beklenen: ışık)
print("YILMAZ".title())     # Yilmaz    (beklenen: Yılmaz)

# Çözüm: upper/lower'dan ÖNCE Türkçe harfleri elle değiştir
sehir = "istanbul"
print(sehir.replace("i", "İ").replace("ı", "I").upper())    # İSTANBUL

kelime = "IŞIK"
print(kelime.replace("I", "ı").replace("İ", "i").lower())   # ışık


# %% Bölüm 10 — Temizlemek ve değiştirmek: strip, replace
giris = "   ayse@example.com   "
print("|" + giris + "|")            # |   ayse@example.com   |
print("|" + giris.strip() + "|")    # |ayse@example.com|

telefon = "0532 123 45 67"
print(telefon.replace(" ", ""))     # 05321234567

ondalik = "3,5"                      # kullanıcı Türkçe alışkanlıkla virgül yazdı
print(float(ondalik.replace(",", ".")) * 2)   # 7.0


# %% Bölüm 11 — Metin içinde arama: in, find, count, startswith, endswith
cumle = "Python öğrenmek çok keyifli. Python her yerde."

print("Python" in cumle)            # True
print("Java" in cumle)              # False
print(cumle.count("Python"))        # 2
print(cumle.find("öğren"))          # 7   -> ilk geçtiği indeks
print(cumle.find("Java"))           # -1  -> bulunamadı
print(cumle.startswith("Py"))       # True

eposta = "ayse@example.com"
print(eposta.endswith(".com"))      # True


# %% Bölüm 12 — Bölmek ve birleştirmek: split, join
tarih = "25.10.2026"
parcalar = tarih.split(".")
print(parcalar)                     # ['25', '10', '2026']  -> bir LİSTE (Hafta 3)
print(parcalar[2])                  # 2026

cumle = "Python öğrenmek çok keyifli"
kelimeler = cumle.split()           # boşluklardan böler
print(kelimeler)                    # ['Python', 'öğrenmek', 'çok', 'keyifli']

print("-".join(parcalar))           # 25-10-2026
print(" ".join(kelimeler).upper())  # PYTHON ÖĞRENMEK ÇOK KEYIFLI -> dikkat: i -> I (Bölüm 9)


# %% Uygulama 1 — İsim ve e-posta biçimlendirme  [GİRİŞ BEKLER]
ham_ad = input("Adınız ve soyadınız: ")          # örnek giriş: "  ayşe YILMAZ "

temiz = ham_ad.strip()
kucuk = temiz.replace("I", "ı").replace("İ", "i").lower()
duzgun = kucuk.title()

ascii_ad = kucuk.replace("ç", "c").replace("ğ", "g").replace("ı", "i")
ascii_ad = ascii_ad.replace("ö", "o").replace("ş", "s").replace("ü", "u")
eposta = ascii_ad.replace(" ", ".") + "@example.com"

parcalar = duzgun.split()
bas_harfler = parcalar[0][0] + parcalar[-1][0]

print(f"{'Ad Soyad':<12}: {duzgun}")
print(f"{'E-posta':<12}: {eposta}")
print(f"{'Baş harfler':<12}: {bas_harfler}")


# %% Uygulama 2 — Hizalı kafe fişi ve Türk lirası biçimi
urun1, adet1, fiyat1 = "Türk kahvesi", 2, 85
urun2, adet2, fiyat2 = "Simit", 1, 30
urun3, adet3, fiyat3 = "Doğum günü pastası", 1, 950

tutar1 = adet1 * fiyat1
tutar2 = adet2 * fiyat2
tutar3 = adet3 * fiyat3
toplam = tutar1 + tutar2 + tutar3

print(f"{'Ürün':<20}{'Adet':>5}{'Tutar':>12}")
print("-" * 37)
print(f"{urun1:<20}{adet1:>5}{tutar1:>12.2f}")
print(f"{urun2:<20}{adet2:>5}{tutar2:>12.2f}")
print(f"{urun3:<20}{adet3:>5}{tutar3:>12.2f}")
print("-" * 37)

toplam_tr = f"{toplam:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
print(f"{'TOPLAM':<25}{toplam_tr:>12} TL")


# =============================================================================
# SINIF İÇİ ALIŞTIRMALARIN ÇÖZÜMLERİ
# =============================================================================

# %% Alıştırma 1 (kolay) — Bir kelimeyi parçala
kelime = "Programlama"
print("İlk harf:", kelime[0])
print("Son harf:", kelime[-1])
print("İlk üç harf:", kelime[:3])
print("Tersten:", kelime[::-1])
print("Uzunluk:", len(kelime))


# %% Alıştırma 2 (kolay-orta) — f-string ile ürün etiketi
urun = "Laptop çantası"
fiyat = 1250
indirim_orani = 0.15
indirimli = fiyat * (1 - indirim_orani)
print(f"{urun}: {indirimli:.2f} TL ({indirim_orani:.0%} indirim)")


# %% Alıştırma 3 (orta) — Hata avı (düzeltilmiş hali)
# Hatalı hali:
#   mesaj = "merhaba dünya"
#   print(mesaj.Upper())
#   print(mesaj[13])
#   print("-".join([2026, 10, 25]))
mesaj = "merhaba dünya"
print(mesaj.upper())
print(mesaj[12])          # ya da mesaj[-1]
print("-".join(["2026", "10", "25"]))


# %% Alıştırma 4 (zor) — Telefon numarası düzenleyici  [GİRİŞ BEKLER]
ham = input("Telefon numarası: ")        # örnek: "0 532 123 45 67"
numara = ham.replace(" ", "").removeprefix("0")
alan, orta = numara[:3], numara[3:6]
son1, son2 = numara[6:8], numara[8:]
duzenli = f"+90 ({alan}) {orta} {son1} {son2}"
print(duzenli)                            # +90 (532) 123 45 67


# %% Ek — Gelecek dersin önizlemesi: gömülü fonksiyonlar
print(len("Python"))       # 6
print(max(3, 9, 4))        # 9
print(round(217.125, 2))   # 217.12
