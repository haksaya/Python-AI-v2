# =============================================================================
# Python Kursu — Ders 7 (Hafta 4, Gün 1)
# Konu: Karşılaştırma ve mantıksal operatörler; if, elif, else
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
#   - input() içeren hücreler klavyeden giriş bekler; farklı değerlerle tekrar çalıştırın.
#   - Girinti (satır başındaki 4 boşluk) Python'da zorunludur; silmeyin.
# =============================================================================


# %% Ödev kontrolü — Ders 6 Ödev 1: not defteri
notlar = {"Ali": 70, "Ece": 85, "Can": 92, "Deniz": 64, "Elif": 78}
notlar["Ali"] = 75
del notlar["Deniz"]
ortalama = sum(notlar.values()) / len(notlar)
birinci = max(notlar, key=notlar.get)
print(f"Ortalama: {ortalama:.1f}")
print(f"En yüksek: {birinci} ({notlar[birinci]})")


# %% Bölüm 1 — Karşılaştırma operatörleri
not_ = 72
gecti = not_ >= 50
print(gecti)
print(type(gecti))
print(not_ == 100, not_ != 100)


# %% Bölüm 2 — Metin, aralık ve üyelik karşılaştırmaları
print("elma" == "Elma")
print("ankara" < "izmir")
print("10" == 10)
yas = 34
print(18 <= yas <= 65)
print("süt" in ["ekmek", "süt"])
print(0.1 + 0.2 == 0.3)


# %% Bölüm 3 — and, or, not
yas = 20
ehliyet = True
print(yas >= 18 and ehliyet)
hafta_sonu = False
tatil = True
print(hafta_sonu or tatil)
print(not ehliyet)


# %% Bölüm 4a — Tuzak: or ile tek tarafı yazmak
renk = "mor"
print(renk == "kırmızı" or "mavi")
print(bool(renk == "kırmızı" or "mavi"))


# %% Bölüm 4b — Doğrusu: iki karşılaştırma ya da in
renk = "mor"
print(renk == "kırmızı" or renk == "mavi")
print(renk in ("kırmızı", "mavi"))


# %% Bölüm 5 — Doğru ve yanlış sayılan değerler (truthy/falsy)
sepet = []
print(bool(sepet))
ad = input("Adınız: ").strip()
print(bool(ad))
print(bool(-3), bool(" "))


# %% Bölüm 5b — Koşulları adlandırmak
yas = 22
ogrenci = True
gun = "Salı"
hafta_ici = gun not in ("Cumartesi", "Pazar")
indirimli = (ogrenci and hafta_ici) or yas >= 65
print("Hafta içi mi?", hafta_ici)
print("İndirim var mı?", indirimli)


# %% Bölüm 6 — if: koşul doğruysa çalış
sicaklik = int(input("Hava kaç derece? "))
if sicaklik < 10:
    print("Mont almayı unutma!")
    print("Atkı da iyi olur.")
print("İyi günler.")


# %% Bölüm 7 — if / else: iki yoldan biri
yas = int(input("Yaşınız: "))
if yas >= 18:
    print("Oy kullanabilirsiniz.")
else:
    kalan = 18 - yas
    print(f"{kalan} yıl sonra oy kullanabilirsiniz.")


# %% Bölüm 8 — Girinti seviyeleri
puan = 85
if puan >= 50:
    print("Geçti")
    if puan >= 85:
        print("Takdir belgesi!")
print("Bitti")


# %% Bölüm 9 — elif: çok seçenekli karar
hiz = int(input("Hızınız (km/sa): "))
if hiz <= 50:
    print("Yasal hız.")
elif hiz <= 60:
    print("Uyarı: sınıra yakınsınız.")
elif hiz <= 80:
    print("Ceza: hız sınırı aşıldı.")
else:
    print("Ağır ceza ve ehliyete el koyma!")


# %% Bölüm 10a — Yanlış sıra
puan = 95
if puan >= 50:
    print("Geçti")
elif puan >= 85:
    print("Pekiyi")


# %% Bölüm 10b — Doğru sıra
puan = 95
if puan >= 85:
    print("Pekiyi")
elif puan >= 50:
    print("Geçti")


# %% Bölüm 11 — Tek satırlık koşullu ifade
puan = 64
durum = "Geçti" if puan >= 50 else "Kaldı"
print(durum)
stok = 0
print("Stokta" if stok > 0 else "Tükendi")


# %% Bölüm 12 — Giriş kontrolü: önce kontrol, sonra çevir
giris = input("Yaşınız: ").strip()
if not giris:
    print("Boş bırakmayın.")
elif not giris.isdigit():
    print("Lütfen yalnızca rakam girin.")
elif not 0 < int(giris) < 120:
    print("Geçerli bir yaş girin.")
else:
    yas = int(giris)
    print(f"Teşekkürler, {yas} yaşındasınız.")


# %% Bölüm 13 — İç içe koşullar
kullanici = "admin"
sifre = "1234"
if kullanici == "admin":
    if sifre == "Py2026!":
        print("Hoş geldiniz.")
    else:
        print("Şifre hatalı.")
else:
    print("Kullanıcı bulunamadı.")


# %% Uygulama 1 — Sayısal not → harf notu
giris = input("Sınav notunuz (0-100): ").strip()

if not giris.isdigit() or int(giris) > 100:
    print("Hatalı giriş: 0-100 arası tam sayı yazın.")
else:
    puan = int(giris)
    if puan >= 90:
        harf = "AA"
    elif puan >= 85:
        harf = "BA"
    elif puan >= 80:
        harf = "BB"
    elif puan >= 75:
        harf = "CB"
    elif puan >= 70:
        harf = "CC"
    elif puan >= 65:
        harf = "DC"
    elif puan >= 60:
        harf = "DD"
    elif puan >= 50:
        harf = "FD"
    else:
        harf = "FF"
    durum = "Geçti" if puan >= 60 else "Kaldı"
    print(f"Notunuz: {puan} → {harf} ({durum})")


# %% Uygulama 2 — Giriş kontrolü (sözlük + koşul)
kullanicilar = {"ayse": "Elma2026", "mehmet": "Kalem!77"}
ad = input("Kullanıcı adı: ").strip().lower()
sifre = input("Şifre: ")
if ad not in kullanicilar:
    print("Böyle bir kullanıcı yok.")
elif kullanicilar[ad] != sifre:
    print("Şifre hatalı.")
else:
    print(f"Hoş geldin, {ad.title()}!")


# %% Alıştırma 1 — çözüm
sayi = int(input("Bir tam sayı: "))
if sayi > 0:
    print("Pozitif")
elif sayi < 0:
    print("Negatif")
else:
    print("Sıfır")
print("Çift" if sayi % 2 == 0 else "Tek")


# %% Alıştırma 2 — çözüm
yas = int(input("Yaşınız: "))
tam = 180
if yas < 12:
    ucret = tam / 2
elif yas >= 65:
    ucret = tam * 0.6
else:
    ucret = tam
print(f"Ödenecek: {ucret:.2f} TL")


# %% Alıştırma 3 — çözüm (düzeltilmiş)
bakiye = float(input("Bakiye: "))
if bakiye > 100:
    print("Alışveriş yapabilirsiniz.")
else:
    print("Yetersiz bakiye.")


# %% Alıştırma 4 — çözüm
sifre = input("Şifre: ")
guclu = True

if len(sifre) < 8:
    print("En az 8 karakter olmalı.")
    guclu = False
if sifre == sifre.lower():
    print("En az bir büyük harf içermeli.")
    guclu = False
if sifre.isalpha():
    print("Yalnızca harften oluşmamalı (rakam ya da sembol ekleyin).")
    guclu = False
if " " in sifre:
    print("Boşluk içermemeli.")
    guclu = False

if guclu:
    print("Güçlü şifre.")


# %% Ek — Gelecek dersin önizlemesi: döngüler
for n in [70, 45, 92]:
    if n >= 50:
        print(n, "Geçti")
