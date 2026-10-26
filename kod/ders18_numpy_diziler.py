# =============================================================================
# Python Kursu — Ders 18 (Hafta 9, Gün 2)
# Konu: NumPy nedir, np.array, dtype ve shape, vektörel işlemler, karşılaştırma, evrensel fonksiyonlar, toplama metotları, dizi oluşturma, rastgele sayılar, matrisler ve eksenler — not ve sıcaklık dizileri
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum (terminalde, sanal ortam etkinken): python -m pip install numpy
#   - Ders materyali NumPy 2.x ile hazırlandı; 1.x sürümlerinde bazı çıktılar biraz farklı görünebilir.
#   - Notlar ve sıcaklıklar örnek amaçlı uydurulmuş değerlerdir.
# =============================================================================


# %% Bölüm 1 — Liste mi, dizi mi?
import numpy as np

liste = [72, 45, 88, 91]
print(liste * 2)            # liste tekrarlanır
dizi = np.array(liste)
print(dizi * 2)             # her eleman 2 ile çarpılır
print(dizi + 5)


# %% Bölüm 2 — Hız karşılaştırması (süreler bilgisayara göre değişir)
import time
import numpy as np

sayilar = list(range(1_000_000))
dizi = np.arange(1_000_000)

bas = time.perf_counter()
kareler_liste = [x * x for x in sayilar]
sure_liste = time.perf_counter() - bas

bas = time.perf_counter()
kareler_dizi = dizi * dizi
sure_dizi = time.perf_counter() - bas

print(f"Liste: {sure_liste*1000:.1f} ms · NumPy: {sure_dizi*1000:.1f} ms")
print(f"NumPy yaklaşık {sure_liste / sure_dizi:.0f} kat hızlı")


# %% Bölüm 3 — Kurulum kontrolü
import numpy as np

print(np.__version__)
print(type(np.array([1, 2, 3])))


# %% Bölüm 4 — np.array ve temel özellikler
import numpy as np

notlar = np.array([72, 45, 88, 91, 60])
print(notlar)
print("dtype:", notlar.dtype)
print("shape:", notlar.shape, "ndim:", notlar.ndim, "size:", notlar.size)
print("İlk not:", notlar[0], "· Son not:", notlar[-1])


# %% Bölüm 5 — Tek tip kuralı
import numpy as np

a = np.array([1, 2, 3])
b = np.array([1, 2.5, 3])
c = np.array([1, 2.5, "3"])
print(a.dtype, b.dtype, c.dtype)
print(b)
print(c)


# %% Bölüm 6 — Sayıyla vektörel işlemler
import numpy as np

fiyatlar = np.array([45.0, 12.5, 650.0, 7.5])
print(fiyatlar * 1.20)            # %20 KDV dahil
print(fiyatlar - 5)
print(fiyatlar / 2)
print(fiyatlar // 10, fiyatlar % 10)


# %% Bölüm 7 — Dizi ile dizi: ağırlıklı ortalama
import numpy as np

vize = np.array([60, 75, 40, 90])
final = np.array([70, 85, 55, 95])
ortalama = vize * 0.4 + final * 0.6
print(ortalama)
print(final - vize)            # her öğrencinin artışı


# %% Bölüm 8 — Karşılaştırma ve mantıksal diziler
import numpy as np

ortalama = np.array([66.0, 81.0, 49.0, 93.0])
gecti = ortalama >= 50
print(gecti)
print(gecti.dtype, gecti.sum(), "öğrenci geçti")
print("Geçme oranı: %", gecti.mean() * 100)


# %% Bölüm 9 — Evrensel fonksiyonlar
import numpy as np

degerler = np.array([4, -9, 16.7, 25])
print(np.abs(degerler))
print(np.sqrt(np.abs(degerler)).round(2))
print(np.round(degerler / 3, 1))


# %% Bölüm 10 — Toplama (özet) metotları
import numpy as np

sicaklik = np.array([17.4, 19.8, 18.1, 16.5, 21.2, 22.0, 20.3])
print("Toplam:", sicaklik.sum().round(1), "· Ortalama:", sicaklik.mean().round(2))
print("En düşük:", sicaklik.min(), "· En yüksek:", sicaklik.max())
print("Standart sapma:", sicaklik.std().round(2), "· Medyan:", np.median(sicaklik))
gunler = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
print("En sıcak gün:", gunler[sicaklik.argmax()], "· En serin gün:", gunler[sicaklik.argmin()])


# %% Bölüm 11 — İndeksleme ve dilimleme
import numpy as np

sicaklik = np.array([17.4, 19.8, 18.1, 16.5, 21.2, 22.0, 20.3])
print(sicaklik[0], sicaklik[-1])
print(sicaklik[:3])            # ilk üç gün
print(sicaklik[-2:])           # hafta sonu
print(sicaklik[::2])           # gün aşırı
sicaklik[3] = 16.9             # düzeltme
print(sicaklik[2:5])


# %% Bölüm 12 — Hazır dizi oluşturma fonksiyonları
import numpy as np

print(np.arange(0, 20, 5))          # range gibi
print(np.linspace(0, 1, 5))         # 0–1 arası eşit aralıklı 5 sayı
print(np.zeros(4), np.ones(3))
print(np.full(5, 7))


# %% Bölüm 13 — Rastgele sayılar
import numpy as np

rng = np.random.default_rng(42)     # tohum: aynı sonuçlar
zarlar = rng.integers(1, 7, size=10)
print(zarlar)
notlar = rng.integers(0, 101, size=5)
print(notlar, notlar.mean())
boylar = rng.normal(170, 8, size=4).round(1)
print(boylar)


# %% Bölüm 14 — İki boyutlu dizi (matris)
import numpy as np

# satırlar: öğrenciler · sütunlar: vize, ödev, final
notlar = np.array([[60, 80, 70],
                   [75, 90, 85],
                   [40, 65, 55],
                   [90, 95, 95]])
print(notlar.shape, notlar.ndim, notlar.size)
print(notlar[1, 2])         # 2. öğrencinin finali
print(notlar[0])            # 1. öğrencinin bütün notları
print(notlar[:, 0])         # bütün öğrencilerin vizesi


# %% Bölüm 15 — axis: sütun mu, satır mı?
import numpy as np

notlar = np.array([[60, 80, 70], [75, 90, 85], [40, 65, 55], [90, 95, 95]])
print("Sınav ortalamaları:", notlar.mean(axis=0).round(1))
print("Öğrenci ortalamaları:", notlar.mean(axis=1).round(1))
print("Genel ortalama:", notlar.mean().round(1))
print("Her sınavın en yükseği:", notlar.max(axis=0))


# %% Bölüm 16 — reshape, zeros((s, k)), eye
import numpy as np

sayilar = np.arange(1, 13)
print(sayilar.reshape(3, 4))
print(np.zeros((2, 3)))
print(np.eye(3, dtype=int))


# %% Uygulama 1 — Sınıf karnesi
import numpy as np

ogrenciler = np.array(["Ece", "Mert", "Zeynep", "Can", "Deniz"])
# sütunlar: vize, ödev, final
notlar = np.array([[60, 80, 70], [75, 90, 85], [40, 65, 55], [90, 95, 95], [55, 40, 48]])
agirlik = np.array([0.3, 0.2, 0.5])

donem = (notlar * agirlik).sum(axis=1)
print("Dönem notları:", donem.round(1))
print("Sınıf ortalaması:", donem.mean().round(1))
print("Birinci:", ogrenciler[donem.argmax()], donem.max().round(1))
print("Kalan sayısı:", (donem < 50).sum())
print("Sınav ortalamaları (vize, ödev, final):", notlar.mean(axis=0).round(1))


# %% Uygulama 2 — Haftalık sıcaklık analizi
import numpy as np

gunler = np.array(["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"])
en_yuksek = np.array([19.8, 18.1, 16.5, 21.2, 22.0, 20.3, 17.9])
en_dusuk = np.array([13.2, 12.7, 11.9, 14.0, 15.1, 13.8, 12.2])
fark = en_yuksek - en_dusuk
fahrenheit = en_yuksek * 9 / 5 + 32
print("Günlük fark:", fark.round(1))
print("En büyük fark:", gunler[fark.argmax()], fark.max().round(1), "°C")
print("°F:", fahrenheit.round(0))
sicak_gunler = en_yuksek > 20
print("20 °C üstü gün sayısı:", sicak_gunler.sum(), "·", gunler[sicak_gunler])


# %% Alıştırma 1 — çözüm
import numpy as np

fiyatlar = np.array([45.0, 120.0, 650.0, 7.5, 99.9])
print("İndirimli:", (fiyatlar * 0.9).round(2))
print("Toplam:", fiyatlar.sum())
print("En pahalı ürünün konumu:", fiyatlar.argmax())
print("100 TL üstü:", (fiyatlar > 100).sum(), "ürün")


# %% Alıştırma 2 — çözüm
import numpy as np

rng = np.random.default_rng(7)
adimlar = rng.integers(2000, 15001, size=30)
print("Ortalama:", adimlar.mean().round(0))
print("En iyi gün:", adimlar.argmax() + 1, "·", adimlar.max(), "adım")
print("10.000 üstü gün oranı: %", ((adimlar > 10000).mean() * 100).round(1))


# %% Alıştırma 3 — çözüm
import numpy as np

magazalar = np.array(["Kadıköy", "Bornova", "Çankaya"])
# sütunlar: Ocak, Şubat, Mart, Nisan (bin TL)
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])
print("Mağaza toplamları:", satis.sum(axis=1))
print("Ay ortalamaları:", satis.mean(axis=0).round(1))
print("En çok satan:", magazalar[satis.sum(axis=1).argmax()])
