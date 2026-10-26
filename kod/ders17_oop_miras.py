# =============================================================================
# Python Kursu — Ders 17 (Hafta 9, Gün 1)
# Konu: Miras (inheritance), super(), metot ezme (override), çok biçimlilik, kapsülleme (_ ve __), @property ve setter, miras ile içerme — şirket bordrosu mini projesi
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum gerekmez.
#   - Maaş ve ücret tutarları kurgusaldır; gerçek bordro hesaplarındaki vergi ve kesintiler bu derste yoktur.
# =============================================================================


# %% Bölüm 1 — Calisan sınıfı ve boş bir alt sınıf
class Calisan:
    unvan = "Çalışan"

    def __init__(self, ad, departman, maas):
        self.ad = ad
        self.departman = departman
        self.maas = maas

    def maas_hesapla(self):
        return self.maas

    def bilgi(self):
        return f"{self.ad} ({self.departman})"


class Yonetici(Calisan):
    pass


y = Yonetici("Ayşe Yılmaz", "Yazılım", 95000)
print(y.bilgi())
print(y.maas_hesapla())


# %% Bölüm 2 — isinstance ve issubclass
class Calisan:
    unvan = "Çalışan"

    def __init__(self, ad, departman, maas):
        self.ad = ad
        self.departman = departman
        self.maas = maas

    def maas_hesapla(self):
        return self.maas

    def bilgi(self):
        return f"{self.ad} ({self.departman})"


class Yonetici(Calisan):
    pass


ali = Calisan("Ali Demir", "Yazılım", 62000)
ayse = Yonetici("Ayşe Yılmaz", "Yazılım", 95000)
print(isinstance(ayse, Yonetici), isinstance(ayse, Calisan))
print(isinstance(ali, Yonetici))
print(issubclass(Yonetici, Calisan), type(ayse).__name__)


# %% Bölüm 3 — super() ile yeni öznitelikler, metot ezme
class Calisan:
    unvan = "Çalışan"

    def __init__(self, ad, departman, maas):
        self.ad = ad
        self.departman = departman
        self.maas = maas

    def maas_hesapla(self):
        return self.maas

    def bilgi(self):
        return f"{self.ad} ({self.departman})"


class Yonetici(Calisan):
    unvan = "Yönetici"

    def __init__(self, ad, departman, maas, prim_orani=0.20):
        super().__init__(ad, departman, maas)
        self.prim_orani = prim_orani
        self.ekip = []

    def ekibe_ekle(self, calisan):
        self.ekip.append(calisan)

    def maas_hesapla(self):
        return self.maas * (1 + self.prim_orani)

    def bilgi(self):
        return super().bilgi() + f" · ekip: {len(self.ekip)} kişi"


ayse = Yonetici("Ayşe Yılmaz", "Yazılım", 95000)
ali = Calisan("Ali Demir", "Yazılım", 62000)
ayse.ekibe_ekle(ali)
print(ayse.ad, ayse.prim_orani, [c.ad for c in ayse.ekip])
print(ayse.bilgi())
print(ayse.maas_hesapla())


# %% Bölüm 4 — Ezilen metotlar ve super().bilgi()
class Calisan:
    unvan = "Çalışan"

    def __init__(self, ad, departman, maas):
        self.ad = ad
        self.departman = departman
        self.maas = maas

    def maas_hesapla(self):
        return self.maas

    def bilgi(self):
        return f"{self.ad} ({self.departman})"


class Yonetici(Calisan):
    unvan = "Yönetici"

    def __init__(self, ad, departman, maas, prim_orani=0.20):
        super().__init__(ad, departman, maas)
        self.prim_orani = prim_orani
        self.ekip = []

    def ekibe_ekle(self, calisan):
        self.ekip.append(calisan)

    def maas_hesapla(self):
        return self.maas * (1 + self.prim_orani)

    def bilgi(self):
        return super().bilgi() + f" · ekip: {len(self.ekip)} kişi"


ali = Calisan("Ali Demir", "Yazılım", 62000)
ayse = Yonetici("Ayşe Yılmaz", "Yazılım", 95000)
ayse.ekibe_ekle(ali)
for kisi in [ali, ayse]:
    print(f"{kisi.unvan:<9}{kisi.bilgi():<40}{kisi.maas_hesapla():>10,.0f}")


# %% Bölüm 5 — Stajyer sınıfı ve çok biçimlilik
class Calisan:
    unvan = "Çalışan"

    def __init__(self, ad, departman, maas):
        self.ad = ad
        self.departman = departman
        self.maas = maas

    def maas_hesapla(self):
        return self.maas

    def bilgi(self):
        return f"{self.ad} ({self.departman})"


class Yonetici(Calisan):
    unvan = "Yönetici"

    def __init__(self, ad, departman, maas, prim_orani=0.20):
        super().__init__(ad, departman, maas)
        self.prim_orani = prim_orani
        self.ekip = []

    def ekibe_ekle(self, calisan):
        self.ekip.append(calisan)

    def maas_hesapla(self):
        return self.maas * (1 + self.prim_orani)

    def bilgi(self):
        return super().bilgi() + f" · ekip: {len(self.ekip)} kişi"


class Stajyer(Calisan):
    unvan = "Stajyer"

    def __init__(self, ad, departman, gunluk_ucret, gun_sayisi):
        super().__init__(ad, departman, maas=0)
        self.gunluk_ucret = gunluk_ucret
        self.gun_sayisi = gun_sayisi

    def maas_hesapla(self):
        return self.gunluk_ucret * self.gun_sayisi


personel = [Calisan("Ali Demir", "Yazılım", 62000),
            Yonetici("Ayşe Yılmaz", "Yazılım", 95000),
            Stajyer("Can Öz", "Yazılım", 900, 20),
            Calisan("Elif Ak", "Pazarlama", 58000)]
toplam = 0
for kisi in personel:
    tutar = kisi.maas_hesapla()       # her nesne kendi metodu
    toplam += tutar
    print(f"{kisi.unvan:<9}{kisi.ad:<13}{tutar:>10,.0f}")
print(f"{'Toplam':<22}{toplam:>10,.0f}")


# %% Bölüm 6 — Neden kapsülleme?
class BankaHesabi:
    def __init__(self, sahip, bakiye=0):
        self.sahip = sahip
        self.bakiye = bakiye

    def cek(self, tutar):
        if tutar > self.bakiye:
            raise ValueError("Yetersiz bakiye.")
        self.bakiye -= tutar


hesap = BankaHesabi("Ayşe", 1000)
hesap.bakiye = -5000          # hiçbir kural çalışmadı!
print(hesap.bakiye)


# %% Bölüm 7 — Tek alt çizgi: _bakiye
class BankaHesabi:
    def __init__(self, sahip, bakiye=0):
        self.sahip = sahip
        self._bakiye = bakiye        # _ : "içeriye ait, dokunma"

    def bakiye_goster(self):
        return self._bakiye


hesap = BankaHesabi("Ayşe", 1000)
print(hesap.bakiye_goster())
print(hesap._bakiye)               # mümkün ama kurala aykırı


# %% Bölüm 8 — Çift alt çizgi: __bakiye
class BankaHesabi:
    def __init__(self, sahip, bakiye=0):
        self.sahip = sahip
        self.__bakiye = bakiye       # ad karıştırma

    def bakiye_goster(self):
        return self.__bakiye


hesap = BankaHesabi("Ayşe", 1000)
print(hesap.bakiye_goster())
try:
    print(hesap.__bakiye)
except AttributeError as hata:
    print("AttributeError:", hata)
print(hesap._BankaHesabi__bakiye)  # gerçek adı (kullanmayın!)


# %% Bölüm 9 — @property ile salt okunur bakiye
class BankaHesabi:
    def __init__(self, sahip, bakiye=0):
        self.sahip = sahip
        self._bakiye = bakiye

    @property
    def bakiye(self):                # okunabilir, yazılamaz
        return self._bakiye

    def yatir(self, tutar):
        if tutar <= 0:
            raise ValueError("Tutar pozitif olmalı.")
        self._bakiye += tutar


hesap = BankaHesabi("Ayşe", 1000)
hesap.yatir(250)
print(hesap.bakiye)                  # parantez yok!
try:
    hesap.bakiye = -5000
except AttributeError as hata:
    print("AttributeError:", hata)


# %% Bölüm 10 — setter ile kontrollü atama ve hesaplanan özellik
class Calisan:
    def __init__(self, ad, maas):
        self.ad = ad
        self.maas = maas             # burada da setter çalışır

    @property
    def maas(self):
        return self._maas

    @maas.setter
    def maas(self, yeni):
        if yeni < 0:
            raise ValueError("Maaş negatif olamaz.")
        self._maas = yeni

    @property
    def yillik_maas(self):           # hesaplanan, salt okunur
        return self._maas * 12


ali = Calisan("Ali Demir", 62000)
ali.maas = 65000                     # setter: kontrol edilerek atanır
print(ali.maas, ali.yillik_maas)
try:
    ali.maas = -1
except ValueError as hata:
    print("Reddedildi:", hata)


# %% Mini proje — Şirket bordrosu (Calisan, Yonetici, Stajyer, Sirket)
class Calisan:
    unvan = "Çalışan"

    def __init__(self, ad, departman, maas):
        self.ad = ad
        self.departman = departman
        self.maas = maas

    def maas_hesapla(self):
        return self.maas

    def bilgi(self):
        return f"{self.ad} ({self.departman})"


class Yonetici(Calisan):
    unvan = "Yönetici"

    def __init__(self, ad, departman, maas, prim_orani=0.20):
        super().__init__(ad, departman, maas)
        self.prim_orani = prim_orani
        self.ekip = []

    def ekibe_ekle(self, calisan):
        self.ekip.append(calisan)

    def maas_hesapla(self):
        return self.maas * (1 + self.prim_orani)

    def bilgi(self):
        return super().bilgi() + f" · ekip: {len(self.ekip)} kişi"


class Stajyer(Calisan):
    unvan = "Stajyer"

    def __init__(self, ad, departman, gunluk_ucret, gun_sayisi):
        super().__init__(ad, departman, maas=0)
        self.gunluk_ucret = gunluk_ucret
        self.gun_sayisi = gun_sayisi

    def maas_hesapla(self):
        return self.gunluk_ucret * self.gun_sayisi


class Sirket:
    def __init__(self, ad):
        self.ad = ad
        self.calisanlar = []

    def ise_al(self, *kisiler):
        self.calisanlar.extend(kisiler)

    def bordro(self, donem):
        print(f"{self.ad} · {donem} bordrosu")
        toplam = 0
        for kisi in self.calisanlar:
            tutar = kisi.maas_hesapla()
            toplam += tutar
            print(f"  {kisi.unvan:<9}{kisi.ad:<14}{tutar:>10,.0f} TL")
        print(f"  {'Toplam':<23}{toplam:>10,.0f} TL")

    def departman_toplamlari(self):
        toplamlar = {}
        for kisi in self.calisanlar:
            toplamlar[kisi.departman] = toplamlar.get(kisi.departman, 0) + kisi.maas_hesapla()
        return toplamlar


sirket = Sirket("Örnek Yazılım A.Ş.")
ayse = Yonetici("Ayşe Yılmaz", "Yazılım", 95000)
ali = Calisan("Ali Demir", "Yazılım", 62000)
can = Stajyer("Can Öz", "Yazılım", 900, 20)
elif_ = Calisan("Elif Ak", "Pazarlama", 58000)
ayse.ekibe_ekle(ali)
ayse.ekibe_ekle(can)
sirket.ise_al(ayse, ali, can, elif_)
sirket.bordro("Ekim 2026")
print(sirket.departman_toplamlari())
print(ayse.bilgi())


# %% Alıştırma 1 — çözüm
import math


class Sekil:
    def __init__(self, ad):
        self.ad = ad

    def alan(self):
        return 0

    def __str__(self):
        return f"{self.ad}: {self.alan():.2f}"


class Daire(Sekil):
    def __init__(self, r):
        super().__init__("Daire")
        self.r = r

    def alan(self):
        return math.pi * self.r ** 2


class Kare(Sekil):
    def __init__(self, a):
        super().__init__("Kare")
        self.a = a

    def alan(self):
        return self.a ** 2


for sekil in [Daire(2), Kare(3), Sekil("Nokta")]:
    print(sekil)


# %% Alıştırma 2 — çözüm
class BankaHesabi:
    def __init__(self, sahip, bakiye=0):
        self.sahip = sahip
        self._bakiye = bakiye

    @property
    def bakiye(self):
        return self._bakiye

    def cek(self, tutar):
        if tutar > self._bakiye:
            raise ValueError("Yetersiz bakiye.")
        self._bakiye -= tutar


class VadeliHesap(BankaHesabi):
    def faiz_ekle(self, oran):
        self._bakiye += self._bakiye * oran

    def cek(self, tutar):
        raise ValueError("Vadeli hesaptan vade dolmadan çekim yapılamaz.")


vadeli = VadeliHesap("Ayşe", 10000)
vadeli.faiz_ekle(0.04)
print(vadeli.bakiye)
try:
    vadeli.cek(100)
except ValueError as hata:
    print("Reddedildi:", hata)


# %% Alıştırma 3 — çözüm
class Calisan:
    def __init__(self, ad, departman, maas):
        self.ad = ad
        self.departman = departman
        self.maas = maas

    @property
    def maas(self):
        return self._maas

    @maas.setter
    def maas(self, yeni):
        if yeni < 0:
            raise ValueError("Maaş negatif olamaz.")
        self._maas = yeni


class Sirket:
    def __init__(self, calisanlar):
        self.calisanlar = calisanlar

    def zam_yap(self, departman, oran):
        for kisi in self.calisanlar:
            if kisi.departman == departman:
                kisi.maas = round(kisi.maas * (1 + oran))

    def en_yuksek(self):
        return max(self.calisanlar, key=lambda k: k.maas)


s = Sirket([Calisan("Ali Demir", "Yazılım", 62000), Calisan("Elif Ak", "Pazarlama", 58000),
            Calisan("Deniz Kara", "Pazarlama", 61000)])
s.zam_yap("Pazarlama", 0.10)
print([(k.ad, k.maas) for k in s.calisanlar])
enb = s.en_yuksek()
print("En yüksek:", enb.ad, enb.maas)
