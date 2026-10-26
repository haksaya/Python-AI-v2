# =============================================================================
# Python Kursu — Ders 16 (Hafta 8, Gün 2)
# Konu: Nesne yönelimli programlamaya giriş: sınıf, nesne, öznitelik, __init__, self, metot, __str__, sınıf değişkeni — ürün, banka hesabı ve alışveriş sepeti
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum gerekmez.
#   - Bazı çıktılarda nesnelerin bellek adresi (0x7f…) görünür; bu değer her çalıştırmada farklıdır.
# =============================================================================


# %% Bölüm 1 — Zaten nesne kullanıyoruz
metin = "merhaba"
liste = [3, 1, 2]
print(type(metin), type(liste))
print(metin.upper(), metin.count("a"))
liste.append(5)
liste.sort()
print(liste)


# %% Bölüm 2 — Sözlük ve fonksiyonlarla ürün
urun = {"ad": "Defter", "fiyat": 45.0, "stok": 10}

def stok_dus(urun, adet):
    urun["stok"] -= adet

def indirimli(urun, oran):
    return urun["fiyat"] * (1 - oran)

stok_dus(urun, 3)
print(urun["stok"], indirimli(urun, 0.2))


# %% Bölüm 3 — İlk sınıf
class Urun:
    pass

defter = Urun()
defter.ad = "Defter"
defter.fiyat = 45.0
print(type(defter))
print(defter.ad, defter.fiyat)


# %% Bölüm 4 — __init__ ile başlangıç değerleri
class Urun:
    def __init__(self, ad, fiyat, stok):
        self.ad = ad
        self.fiyat = fiyat
        self.stok = stok

defter = Urun("Defter", 45.0, 10)
kalem = Urun("Kalem", 12.5, 40)
print(defter.ad, defter.fiyat, defter.stok)
print(kalem.ad, kalem.fiyat, kalem.stok)


# %% Bölüm 5 — Varsayılan değerler
class Urun:
    def __init__(self, ad, fiyat, stok=0, kategori="Genel"):
        self.ad = ad
        self.fiyat = fiyat
        self.stok = stok
        self.kategori = kategori

silgi = Urun("Silgi", 7.5)
canta = Urun("Çanta", 650.0, stok=4, kategori="Aksesuar")
print(silgi.ad, silgi.stok, silgi.kategori)
print(canta.ad, canta.stok, canta.kategori)


# %% Bölüm 6 — Metotlar
class Urun:
    def __init__(self, ad, fiyat, stok=0):
        self.ad = ad
        self.fiyat = fiyat
        self.stok = stok

    def indirimli_fiyat(self, oran):
        return round(self.fiyat * (1 - oran), 2)

    def stok_dus(self, adet):
        if adet > self.stok:
            raise ValueError(f"Yetersiz stok: {self.stok} adet var.")
        self.stok -= adet

    def stok_degeri(self):
        return self.fiyat * self.stok


defter = Urun("Defter", 45.0, 10)
print(defter.indirimli_fiyat(0.2))
defter.stok_dus(3)
print(defter.stok, defter.stok_degeri())


# %% Bölüm 7 — Metot çağrısının arka planı
class Urun:
    def __init__(self, ad, fiyat, stok=0):
        self.ad = ad
        self.fiyat = fiyat
        self.stok = stok

    def indirimli_fiyat(self, oran):
        return round(self.fiyat * (1 - oran), 2)

    def stok_dus(self, adet):
        if adet > self.stok:
            raise ValueError(f"Yetersiz stok: {self.stok} adet var.")
        self.stok -= adet

    def stok_degeri(self):
        return self.fiyat * self.stok


defter = Urun("Defter", 45.0, 10)
defter.stok_dus(2)
Urun.stok_dus(defter, 2)  # aynı işlem, uzun yazım
print(defter.stok)


# %% Bölüm 8 — BankaHesabi sınıfı ve kullanımı
class BankaHesabi:
    def __init__(self, sahip, bakiye=0.0):
        self.sahip = sahip
        self.bakiye = bakiye

    def yatir(self, tutar):
        if tutar <= 0:
            raise ValueError("Tutar pozitif olmalı.")
        self.bakiye += tutar

    def cek(self, tutar):
        if tutar <= 0:
            raise ValueError("Tutar pozitif olmalı.")
        if tutar > self.bakiye:
            raise ValueError(f"Yetersiz bakiye ({self.bakiye:.2f} TL).")
        self.bakiye -= tutar


ayse = BankaHesabi("Ayşe Yılmaz", 1000)
mehmet = BankaHesabi("Mehmet Kaya")
ayse.yatir(250)
mehmet.yatir(400)
ayse.cek(300)
print(ayse.sahip, ayse.bakiye)
print(mehmet.sahip, mehmet.bakiye)
for islem, tutar in [(mehmet.cek, 1000), (ayse.yatir, -50)]:
    try:
        islem(tutar)
    except ValueError as hata:
        print("Reddedildi:", hata)


# %% Bölüm 9 — Hareket geçmişi tutan hesap
from datetime import date


class BankaHesabi:
    def __init__(self, sahip, bakiye=0.0):
        self.sahip = sahip
        self.bakiye = bakiye
        self.hareketler = []          # her nesnenin kendi listesi

    def yatir(self, tutar):
        if tutar <= 0:
            raise ValueError("Tutar pozitif olmalı.")
        self.bakiye += tutar
        self.hareketler.append((date(2026, 10, 26), "Yatırma", tutar))

    def cek(self, tutar):
        if tutar <= 0 or tutar > self.bakiye:
            raise ValueError("Geçersiz tutar ya da yetersiz bakiye.")
        self.bakiye -= tutar
        self.hareketler.append((date(2026, 10, 26), "Çekme", -tutar))

    def ekstre(self):
        print(f"Hesap: {self.sahip}")
        for tarih, tur, tutar in self.hareketler:
            print(f"  {tarih}  {tur:<8}{tutar:>9.2f}")
        print(f"  Bakiye: {self.bakiye:.2f} TL")


hesap = BankaHesabi("Ayşe Yılmaz", 1000)
hesap.yatir(250)
hesap.cek(300)
hesap.ekstre()


# %% Bölüm 10 — __str__ ile okunaklı yazdırma
class Urun:
    def __init__(self, ad, fiyat, stok=0):
        self.ad = ad
        self.fiyat = fiyat
        self.stok = stok

    def __str__(self):
        return f"{self.ad} — {self.fiyat:.2f} TL ({self.stok} adet)"


class UrunEski:
    def __init__(self, ad):
        self.ad = ad


print(UrunEski("Defter"))
defter = Urun("Defter", 45, 10)
print(defter)
print(f"Sepete eklendi: {defter}")


# %% Bölüm 11 — Sınıf değişkenleri
class BankaHesabi:
    banka = "Python Bankası"     # sınıf değişkeni: hepsi paylaşır
    hesap_sayisi = 0

    def __init__(self, sahip):
        self.sahip = sahip           # örnek değişkeni: her nesneye ait
        BankaHesabi.hesap_sayisi += 1
        self.no = BankaHesabi.hesap_sayisi


a = BankaHesabi("Ayşe")
b = BankaHesabi("Mehmet")
print(a.banka, "|", a.sahip, a.no, "|", b.sahip, b.no)
print("Toplam hesap:", BankaHesabi.hesap_sayisi)


# %% Bölüm 12 — Nesne listeleri
class Urun:
    def __init__(self, ad, fiyat, stok=0):
        self.ad = ad
        self.fiyat = fiyat
        self.stok = stok

    def stok_degeri(self):
        return self.fiyat * self.stok


urunler = [Urun("Defter", 45.0, 10), Urun("Kalem", 12.5, 40),
           Urun("Çanta", 650.0, 2), Urun("Silgi", 7.5, 0)]
toplam = sum(u.stok_degeri() for u in urunler)
print(f"Toplam stok değeri: {toplam:.2f} TL")
print("Stokta olmayanlar:", [u.ad for u in urunler if u.stok == 0])
en_pahali = urunler[0]
for u in urunler:
    if u.fiyat > en_pahali.fiyat:
        en_pahali = u
print("En pahalı:", en_pahali.ad)


# %% Uygulama — Alışveriş sepeti (Urun ve Sepet sınıfları)
class Urun:
    def __init__(self, ad, fiyat):
        self.ad = ad
        self.fiyat = fiyat


class Sepet:
    def __init__(self, musteri):
        self.musteri = musteri
        self.kalemler = []            # (Urun, adet) demetleri

    def ekle(self, urun, adet=1):
        self.kalemler.append((urun, adet))

    def toplam(self):
        return sum(urun.fiyat * adet for urun, adet in self.kalemler)

    def indirim_uygula(self, kod):
        indirimler = {"OGRENCI10": 0.10, "YILBASI20": 0.20}
        oran = indirimler.get(kod.upper(), 0)
        return round(self.toplam() * (1 - oran), 2), oran

    def fis(self, kod=""):
        print(f"Müşteri: {self.musteri}")
        for urun, adet in self.kalemler:
            print(f"  {adet} x {urun.ad:<8}{urun.fiyat * adet:>9.2f}")
        tutar, oran = self.indirim_uygula(kod)
        print(f"  Ara toplam: {self.toplam():.2f}  İndirim: %{oran * 100:.0f}")
        print(f"  Ödenecek: {tutar:.2f} TL")


defter, kalem = Urun("Defter", 45.0), Urun("Kalem", 12.5)
sepet = Sepet("Zeynep")
sepet.ekle(defter, 3)
sepet.ekle(kalem, 4)
sepet.fis("ogrenci10")


# %% Alıştırma 1 — çözüm
class Dikdortgen:
    def __init__(self, en, boy):
        self.en = en
        self.boy = boy

    def alan(self):
        return self.en * self.boy

    def cevre(self):
        return 2 * (self.en + self.boy)

    def kare_mi(self):
        return self.en == self.boy


masa = Dikdortgen(120, 80)
fayans = Dikdortgen(30, 30)
print(masa.alan(), masa.cevre(), masa.kare_mi())
print(fayans.alan(), fayans.cevre(), fayans.kare_mi())


# %% Alıştırma 2 — çözüm
class Ogrenci:
    def __init__(self, ad, numara):
        self.ad = ad
        self.numara = numara
        self.notlar = []

    def not_ekle(self, not_):
        if not 0 <= not_ <= 100:
            raise ValueError("Not 0 ile 100 arasında olmalı.")
        self.notlar.append(not_)

    def ortalama(self):
        if not self.notlar:
            return 0
        return sum(self.notlar) / len(self.notlar)

    def durum(self):
        return "Geçti" if self.ortalama() >= 50 else "Kaldı"

    def __str__(self):
        ort = self.ortalama()
        return f"{self.numara} {self.ad}: {ort:.1f} ({self.durum()})"


ece = Ogrenci("Ece", 1024)
for n in [72, 45, 88]:
    ece.not_ekle(n)
print(ece)
try:
    ece.not_ekle(120)
except ValueError as hata:
    print("Hata:", hata)


# %% Alıştırma 3 — çözüm
class Urun:
    def __init__(self, ad, fiyat):
        self.ad = ad
        self.fiyat = fiyat


class Sepet:
    def __init__(self):
        self.kalemler = {}            # ürün adı → [Urun, adet]

    def ekle(self, urun, adet=1):
        if urun.ad in self.kalemler:
            self.kalemler[urun.ad][1] += adet
        else:
            self.kalemler[urun.ad] = [urun, adet]

    def cikar(self, urun_adi):
        if self.kalemler.pop(urun_adi, None) is None:
            print(f"{urun_adi} sepette yok.")

    def urun_sayisi(self):
        return sum(adet for _, adet in self.kalemler.values())

    def toplam(self):
        return sum(urun.fiyat * adet
                   for urun, adet in self.kalemler.values())


defter, kalem = Urun("Defter", 45.0), Urun("Kalem", 12.5)
sepet = Sepet()
sepet.ekle(defter, 2)
sepet.ekle(kalem)
sepet.ekle(defter)          # tekrar: adet 3 olmalı
print(sepet.urun_sayisi(), sepet.toplam())
sepet.cikar("Kalem")
sepet.cikar("Silgi")
print(sepet.urun_sayisi(), sepet.toplam())
