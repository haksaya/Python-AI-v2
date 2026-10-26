# =============================================================================
# Python Kursu — Ders 19 (Hafta 10, Gün 1)
# Konu: Matrislerle dört işlem, yayma (broadcasting), matris çarpımı, cumsum/diff, NaN, filtreleme (boolean indexing), & | ~, np.where, sıralama, birleştirme, kopya ve görünüm — mağaza × ay satış raporu
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum: python -m pip install numpy (Ders 18'de kuruldu).
#   - Satış rakamları örnek amaçlı uydurulmuştur (bin TL).
# =============================================================================


# %% Ödev kontrolü — 6000 zar atışı
import numpy as np

rng = np.random.default_rng(2026)
zarlar = rng.integers(1, 7, size=6000)
for yuz in range(1, 7):
    print(yuz, (zarlar == yuz).sum())


# %% Bölüm 1 — Aynı şekilli iki matris
import numpy as np

bu_yil = np.array([[120, 135, 128, 150], [98, 110, 105, 120], [140, 138, 152, 160]])
gecen_yil = np.array([[110, 120, 125, 130], [100, 104, 98, 112], [130, 140, 135, 150]])
fark = bu_yil - gecen_yil
buyume = (fark / gecen_yil * 100).round(1)
print(fark)
print(buyume)


# %% Bölüm 2 — Yayma: satır vektörü (her ayın hedefi)
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

hedef_ay = np.array([125, 125, 130, 140])      # her ay için hedef
print(satis - hedef_ay)


# %% Bölüm 3 — Yayma: sütun vektörü (her mağazanın hedefi)
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

hedef_magaza = np.array([130, 105, 145]).reshape(-1, 1)   # (3, 1)
print(hedef_magaza.shape)
print(satis - hedef_magaza)


# %% Bölüm 4 — Transpoz (.T)
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

print(satis.T)
print(satis.T.shape)


# %% Bölüm 5 — Matris çarpımı: adet @ fiyat
import numpy as np

urunler = np.array(["Defter", "Kalem", "Çanta"])
fiyat = np.array([45.0, 12.5, 650.0])          # ürün başına TL
# satırlar: mağazalar · sütunlar: ürünlerden satılan adet
adet = np.array([[30, 120, 4],
                 [25,  80, 6],
                 [40, 150, 2]])
ciro = adet @ fiyat
print(ciro)
print("Elle (Kadıköy):", 30 * 45.0 + 120 * 12.5 + 4 * 650.0)


# %% Bölüm 6 — @ ile ağırlıklı ortalama (Ders 18 bağlantısı)
import numpy as np

notlar = np.array([[60, 80, 70], [75, 90, 85], [40, 65, 55]])
agirlik = np.array([0.3, 0.2, 0.5])
print((notlar * agirlik).sum(axis=1))
print(notlar @ agirlik)


# %% Bölüm 7 — cumsum ve diff
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

kadikoy = satis[0]
print("Aylık:", kadikoy)
print("Kümülatif:", kadikoy.cumsum())
print("Aydan aya fark:", np.diff(kadikoy))
print("Aylık büyüme %:", (np.diff(kadikoy) / kadikoy[:-1] * 100).round(1))
print("Mağaza kümülatifleri:")
print(satis.cumsum(axis=1))


# %% Bölüm 8 — Eksik veri: np.nan
import numpy as np

olcum = np.array([21.5, np.nan, 23.0, 22.4, np.nan])
print(olcum.mean())                 # nan "bulaşıcıdır"
print(np.nanmean(olcum).round(2))   # nan'ları yok say
print(np.isnan(olcum), np.isnan(olcum).sum(), "eksik")


# %% Bölüm 9 — Filtreleme: dizi[maske]
import numpy as np

kadikoy = np.array([120, 135, 128, 150])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
maske = kadikoy > 130
print(maske)
print(kadikoy[maske])
print(aylar[maske])
print(kadikoy[kadikoy < 125])


# %% Bölüm 10 — Koşulları birleştirmek: & | ~
import numpy as np

kadikoy = np.array([120, 135, 128, 150])
print(kadikoy[(kadikoy > 125) & (kadikoy < 140)])   # ve
print(kadikoy[(kadikoy < 125) | (kadikoy > 140)])   # veya
print(kadikoy[~(kadikoy > 130)])                    # değil


# %% Bölüm 11 — İki boyutlu filtreleme ve satır seçme
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

print(satis[satis > 130])                   # 2B maske → 1B sonuç
print((satis > 130).sum(axis=1))            # mağaza başına kaç ay
print(magazalar[satis[:, 3] > 130])         # Nisan'da 130'u geçenler
print(satis[satis.sum(axis=1) > 480])       # toplamı 480'i geçen mağazalar


# %% Bölüm 12 — np.where
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

hedef = 125
durum = np.where(satis >= hedef, "Tuttu", "Kaldı")
print(durum)
duzeltilmis = np.where(satis > 150, 150, satis)      # üst sınır
print(duzeltilmis)
satirlar, sutunlar = np.where(satis < 105)
print("Hedefin çok altı:", magazalar[satirlar], aylar[sutunlar])


# %% Bölüm 13 — Maske ile atama: veri temizleme
import numpy as np

olcum = np.array([21.5, -999.0, 23.0, 22.4, 85.0])   # -999: sensör hatası kodu
olcum[olcum == -999] = np.nan
olcum[olcum > 50] = np.nan                            # imkânsız değer
print(olcum)
print("Ortalama:", np.nanmean(olcum).round(2))


# %% Bölüm 14 — sort ve argsort
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

toplam = satis.sum(axis=1)
print(np.sort(toplam))                  # küçükten büyüğe
print(np.sort(toplam)[::-1])            # büyükten küçüğe
sira = np.argsort(toplam)[::-1]         # büyükten küçüğe KONUMLAR
print(sira, magazalar[sira])
print(satis[sira])                      # satırları toplama göre sırala


# %% Bölüm 15 — vstack ve hstack: satır ve sütun eklemek
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

izmit = np.array([[105, 112, 118, 125]])          # yeni mağaza (1, 4)
satis2 = np.vstack([satis, izmit])
magazalar2 = np.append(magazalar, "İzmit")
print(satis2.shape, magazalar2)
mayis = np.array([155, 118, 165, 130]).reshape(-1, 1)   # yeni ay (4, 1)
satis3 = np.hstack([satis2, mayis])
print(satis3.shape)
print(satis3)


# %% Bölüm 16 — Görünüm ve kopya
import numpy as np

satis = np.array([120, 135, 128, 150])
ilk_iki = satis[:2]          # görünüm (view)
ilk_iki[0] = 0
print(satis)                 # orijinal de değişti!
yedek = satis.copy()         # bağımsız kopya
yedek[1] = 999
print(satis)
print(yedek)


# %% Uygulama — Mağaza × ay satış raporu
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
aylar = np.array(["Oca", "Şub", "Mar", "Nis"])
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])

gecen_yil = np.array([[110, 120, 125, 130], [100, 104, 98, 112], [130, 140, 135, 150]])
hedef = np.array([130, 105, 145]).reshape(-1, 1)

toplam = satis.sum(axis=1)
buyume = ((toplam - gecen_yil.sum(axis=1)) / gecen_yil.sum(axis=1) * 100).round(1)
hedef_ay_sayisi = (satis >= hedef).sum(axis=1)
en_iyi_ay = aylar[satis.argmax(axis=1)]

print(f"{'Mağaza':<9}{'Toplam':>7}{'Büyüme%':>9}{'Hedef':>7}  En iyi ay")
for i in np.argsort(toplam)[::-1]:
    print(f"{magazalar[i]:<9}{toplam[i]:>7}{buyume[i]:>9}{hedef_ay_sayisi[i]:>5}/4  {en_iyi_ay[i]}")
print("Zincir toplamı:", toplam.sum(), "· Düşüş görülen hücre sayısı:", (satis < gecen_yil).sum())


# %% Alıştırma 1 — çözüm
import numpy as np

gunler = np.array(["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"])
sicaklik = np.array([19.8, 18.1, 16.5, 21.2, 22.0, 20.3, 17.9])
sicak = sicaklik > 20
print(gunler[sicak], sicaklik[sicak])
print(((sicaklik >= 18) & (sicaklik <= 21)).sum(), "gün 18–21 °C")


# %% Alıştırma 2 — çözüm
import numpy as np

notlar = np.array([72, -1, 45, 88, -1, 60, 38]).astype(float)
girmedi = notlar == -1
notlar[girmedi] = np.nan
print("Ortalama:", np.nanmean(notlar).round(1), "· Girmeyen:", girmedi.sum())
etiket = np.where(girmedi, "Girmedi", np.where(notlar >= 50, "Geçti", "Kaldı"))
print(etiket)


# %% Alıştırma 3 — çözüm
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
fiyat = np.array([45.0, 12.5, 650.0])
adet = np.array([[30, 120, 4], [25, 80, 6], [40, 150, 2]])
ciro = adet @ fiyat
print("Ciro:", ciro)
print("Ürün başına adet:", adet.sum(axis=0))
print("En çok ciro:", magazalar[ciro.argmax()])
print("Ortalamanın üstü:", magazalar[ciro > ciro.mean()])
