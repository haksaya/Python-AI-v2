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

# --- 1) Veriler ---
# Birden fazla değişkene tek satırda değer atama (çoklu atama / tuple unpacking).
# Sıra önemlidir: soldaki 1. değişken sağdaki 1. değeri alır, 2. değişken 2. değeri alır...
urun1, adet1, fiyat1 = "Türk kahvesi", 2, 85        # ürün adı (str), adet (int), birim fiyat (int)
urun2, adet2, fiyat2 = "Simit", 1, 30
urun3, adet3, fiyat3 = "Doğum günü pastası", 1, 950

# --- 2) Hesaplamalar ---
# Her satırın tutarı = adet × birim fiyat
tutar1 = adet1 * fiyat1      # 2 * 85  = 170
tutar2 = adet2 * fiyat2      # 1 * 30  = 30
tutar3 = adet3 * fiyat3      # 1 * 950 = 950
toplam = tutar1 + tutar2 + tutar3   # 170 + 30 + 950 = 1150

# --- 3) Fişin başlık satırı ---
# f-string içinde {değer:biçim} yazılır. İki noktadan (:) sonrası "biçim belirteci"dir.
#   <  : sola hizala  (metin sola yaslanır, kalan boşluk SAĞA eklenir)
#   >  : sağa hizala  (metin sağa yaslanır, kalan boşluk SOLA eklenir)
#   ^  : ortala       (bu kodda kullanılmadı ama aynı mantık)
#   Sayı: alanın toplam genişliği (kaç karakterlik yer ayrılacağı)
#
# {'Ürün':<20}  -> "Ürün" yazısını 20 karakterlik alana SOLA yaslı yaz
# {'Adet':>5}   -> "Adet" yazısını 5 karakterlik alana SAĞA yaslı yaz
# {'Tutar':>12} -> "Tutar" yazısını 12 karakterlik alana SAĞA yaslı yaz
# Toplam genişlik: 20 + 5 + 12 = 37 karakter
# Not: Süslü parantez içinde tek tırnak kullanıldı çünkü f-string çift tırnakla açıldı.
print(f"{'Ürün':<20}{'Adet':>5}{'Tutar':>12}")

# "-" * 37 -> tire karakterini 37 kez tekrarlar; başlık genişliğiyle aynı uzunlukta çizgi çizer
print("-" * 37)

# --- 4) Ürün satırları ---
# {urun1:<20}    -> ürün adını 20 karakterlik alana sola yaslı yaz (metinler genelde sola yaslanır)
# {adet1:>5}     -> adedi 5 karakterlik alana sağa yaslı yaz (sayılar genelde sağa yaslanır,
#                   böylece basamaklar alt alta düzgün hizalanır)
# {tutar1:>12.2f}-> tutarı 12 karakterlik alana sağa yaslı yaz
#                   .2f : "f" = ondalıklı sayı (float) biçimi, ".2" = virgülden sonra 2 basamak
#                   Örn. 170 -> "170.00"
print(f"{urun1:<20}{adet1:>5}{tutar1:>12.2f}")
print(f"{urun2:<20}{adet2:>5}{tutar2:>12.2f}")
print(f"{urun3:<20}{adet3:>5}{tutar3:>12.2f}")
print("-" * 37)

# --- 5) Toplamı Türk lirası biçimine çevirme ---
# Python varsayılan olarak İngilizce biçim kullanır:  1,150.00  (binlik ayırıcı ",", ondalık ".")
# Türkçede ise tam tersi:                            1.150,00  (binlik ayırıcı ".", ondalık ",")
#
# f"{toplam:,.2f}" -> ","  : binlik ayırıcı ekle
#                     ".2f": 2 ondalık basamaklı float
#                     Sonuç: "1,150.00"
#
# Ardından üç adımlı yer değiştirme (replace) yapılır:
#   .replace(",", "#")  -> "1#150.00"  (virgülleri geçici olarak # yap)
#   .replace(".", ",")  -> "1#150,00"  (noktayı virgül yap -> ondalık ayırıcı)
#   .replace("#", ".")  -> "1.150,00"  (# işaretlerini nokta yap -> binlik ayırıcı)
# Neden "#" kullanıldı? Doğrudan virgülü noktaya çevirseydik, sonra noktaları virgüle
# çevirirken az önce oluşturduğumuz noktalar da virgül olurdu. "#" geçici bir yer tutucudur.
toplam_tr = f"{toplam:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")

# --- 6) Toplam satırı ---
# {'TOPLAM':<25} -> "TOPLAM" yazısını 25 karakterlik alana sola yaslı yaz
# {toplam_tr:>12}-> "1.150,00" metnini 12 karakterlik alana sağa yaslı yaz
# 25 + 12 = 37 -> üstteki satırlarla aynı genişlik, böylece tutar sütunuyla hizalanır
#                 (20 + 5 = 25: ürün ve adet sütunlarının toplam genişliği)
# Sona " TL" eklenerek para birimi gösterilir.
# Not: toplam_tr artık bir metin (str) olduğu için burada .2f kullanılmaz.
print(f"{'TOPLAM':<25}{toplam_tr:>12} TL")

# Beklenen çıktı:
# Ürün                 Adet       Tutar
# -------------------------------------
# Türk kahvesi            2      170.00
# Simit                   1       30.00
# Doğum günü pastası      1      950.00
# -------------------------------------
# TOPLAM                       1.150,00 TL


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
