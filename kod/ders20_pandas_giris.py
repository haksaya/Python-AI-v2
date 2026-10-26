# =============================================================================
# Python Kursu — Ders 20 (Hafta 10, Gün 2)
# Konu: Pandas nedir, Series ve DataFrame, index ve columns, veri tipleri, head/info/describe, sütun seçme, loc/iloc, yeni sütun, sort_values, value_counts — kitaplık tablosu
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum (sanal ortam etkinken): python -m pip install pandas
#   - Ders materyali Pandas 3.x ile hazırlandı. Pandas 2.x'te metin sütunlarının tipi 'str' yerine 'object' görünür; diğer her şey aynı çalışır.
#   - Kitap bilgileri (yazar, ilk yayın yılı) gerçek; puan ve okundu sütunları örnek amaçlıdır.
# =============================================================================


# %% Ödev kontrolü — Kantin satışları (örnek veri)
import numpy as np

urunler = np.array(["Simit", "Tost", "Ayran", "Su", "Kek"])
fiyat = np.array([15.0, 45.0, 20.0, 10.0, 25.0])
# satırlar: günler (Pzt–Cum) · sütunlar: ürünler
adet = np.array([[40, 22, 30, 50, 12], [35, 25, 28, 45, 0],
                 [42, 30, 35, 60, 15], [38, 18, 25, 40, 10],
                 [50, 35, 40, 70, 20]])
print("Günlük ciro:", adet @ fiyat)
print("En çok satan:", urunler[adet.sum(axis=0).argmax()])


# %% Bölüm 1 — Kurulum kontrolü
import pandas as pd

print(pd.__version__)


# %% Bölüm 2 — Series: adlandırılmış tek sütun
import pandas as pd

notlar = pd.Series([72, 45, 88, 91], index=["Ece", "Mert", "Zeynep", "Can"])
print(notlar)
print(notlar["Zeynep"], notlar.iloc[0])
print(notlar.index.tolist(), notlar.values)


# %% Bölüm 3 — Series ile işlem ve ad hizalaması
import pandas as pd

vize = pd.Series([60, 75, 40], index=["Ece", "Mert", "Zeynep"])
final = pd.Series([85, 70, 55], index=["Mert", "Ece", "Can"])
print((vize * 0.4 + final * 0.6).round(1))
print(vize[vize >= 50])
print(vize.mean(), vize.max(), vize.idxmax())


# %% Bölüm 4 — Sözlükten Series
import pandas as pd

nufus = pd.Series({"İstanbul": 15.7, "Ankara": 5.8, "İzmir": 4.5})
print(nufus)
print("Ankara" in nufus, nufus.sum().round(1))
nufus["Bursa"] = 3.2            # yeni eleman
print(nufus.sort_values(ascending=False))


# %% Bölüm 5 — DataFrame: sözlükten tablo
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Sait Faik"],
    "yil": [1972, 1955, 1936],
    "puan": [5, 4, 3],
})
print(kitaplar)


# %% Bölüm 6 — DataFrame'in parçaları
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

print(kitaplar.shape)
print(kitaplar.columns.tolist())
print(kitaplar.index)
print(type(kitaplar["yil"]))


# %% Bölüm 7 — Sözlük listesinden ve NumPy'den DataFrame
import numpy as np
import pandas as pd

# 1) Sözlük listesinden (her sözlük bir satır)
kayitlar = [{"ad": "Kalem", "fiyat": 12.5, "stok": 40},
            {"ad": "Defter", "fiyat": 45.0, "stok": 10}]
urunler = pd.DataFrame(kayitlar)
print(urunler)

# 2) NumPy matrisinden (Ders 19)
satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])
df = pd.DataFrame(satis, index=["Kadıköy", "Bornova", "Çankaya"],
                  columns=["Oca", "Şub", "Mar", "Nis"])
print(df)


# %% Bölüm 8 — Veri tipleri ve astype
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

print(kitaplar.dtypes.astype(str).to_dict())
kitaplar["yil"] = kitaplar["yil"].astype(float)
print(kitaplar["yil"].dtype)
tarih = pd.to_datetime(pd.Series(["2026-10-20", "2026-10-27"]))
print(tarih.dt.day_name().tolist())


# %% Bölüm 9 — head ve tail
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

print(kitaplar.head(3))
print(kitaplar.tail(2))


# %% Bölüm 10 — info
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

kitaplar.info()


# %% Bölüm 11a — describe (sayısal)
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

print(kitaplar.describe())


# %% Bölüm 11b — describe (metin; Pandas 2: include="object")
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

print(kitaplar.describe(include="str"))


# %% Bölüm 12 — Sütun seçme
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

print(kitaplar["yazar"].head(3))
print(kitaplar[["ad", "puan"]].head(3))
print(kitaplar["puan"].mean())


# %% Bölüm 13 — set_index, loc ve iloc
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

kitaplar = kitaplar.set_index("ad")
print(kitaplar.loc["İnce Memed"])                         # bir satır (adla)
print(kitaplar.loc["Semaver", "yazar"])                   # hücre
print(kitaplar.iloc[0, 1], "|", kitaplar.iloc[-1].name)   # konumla
print(kitaplar.loc[["Semaver", "Tutunamayanlar"], ["yil", "puan"]])


# %% Bölüm 14 — Yeni sütun, drop, rename
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

kitaplar["yas"] = 2026 - kitaplar["yil"]             # yeni sütun: vektörel
kitaplar["klasik"] = kitaplar["yas"] >= 50
kitaplar = kitaplar.drop(columns=["okundu"])
kitaplar = kitaplar.rename(columns={"yil": "ilk_yayin"})
print(kitaplar.head(4))


# %% Bölüm 15a — sort_values
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

print(kitaplar.sort_values("puan", ascending=False).head(3)[["ad", "puan"]])
cift = kitaplar.sort_values(["puan", "yil"], ascending=[False, True])
print(cift[["ad", "puan", "yil"]].head(3))


# %% Bölüm 15b — value_counts, unique, nunique
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

print(kitaplar["yazar"].value_counts().head(3))
print(kitaplar["tur"].unique().tolist(), kitaplar["yazar"].nunique())


# %% Bölüm 16 — Filtreleme önizlemesi
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

okunmus = kitaplar[kitaplar["okundu"]]
print(okunmus[["ad", "puan"]])
print(kitaplar[(kitaplar["puan"] >= 4) & (kitaplar["yil"] < 1960)]["ad"].tolist())


# %% Uygulama — Kitaplık analizi (sonunda kitaplar.csv kaydedilir)
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["Tutunamayanlar", "İnce Memed", "Saatleri Ayarlama Enstitüsü", "Kürk Mantolu Madonna",
           "Puslu Kıtalar Atlası", "Kuyucaklı Yusuf", "Benim Adım Kırmızı", "Semaver"],
    "yazar": ["Oğuz Atay", "Yaşar Kemal", "Ahmet Hamdi Tanpınar", "Sabahattin Ali",
              "İhsan Oktay Anar", "Sabahattin Ali", "Orhan Pamuk", "Sait Faik Abasıyanık"],
    "yil": [1972, 1955, 1961, 1943, 1995, 1937, 1998, 1936],
    "tur": ["roman", "roman", "roman", "roman", "roman", "roman", "roman", "öykü"],
    "puan": [5, 4, 5, 4, 4, 3, 3, 3],
    "okundu": [True, True, False, True, True, False, True, False],
})

kitaplar["yas"] = 2026 - kitaplar["yil"]
print("Kitap sayısı:", len(kitaplar), "· Ortalama puan:", kitaplar["puan"].mean())
print("Okunma oranı: %", kitaplar["okundu"].mean() * 100)
print("En eski:", kitaplar.loc[kitaplar["yil"].idxmin(), "ad"])
print("Puanı 5 olanlar:", kitaplar.loc[kitaplar["puan"] == 5, "ad"].tolist())
print(kitaplar["tur"].value_counts().to_dict())
okunacak = kitaplar[~kitaplar["okundu"]].sort_values("puan", ascending=False)
print("Sıradaki okuma listesi:")
print(okunacak[["ad", "yazar", "puan"]].to_string(index=False))
kitaplar.to_csv("kitaplar.csv", index=False)


# %% Alıştırma 1 — çözüm
import pandas as pd

sehirler = pd.DataFrame({
    "sehir": ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"],
    "plaka": ["34", "06", "35", "16", "07"],
    "bolge": ["Marmara", "İç Anadolu", "Ege", "Marmara", "Akdeniz"],
})
print(sehirler.shape)
print(sehirler.dtypes)
print(sehirler[sehirler["bolge"] == "Marmara"]["sehir"].tolist())


# %% Alıştırma 2 — çözüm
import pandas as pd

notlar = pd.DataFrame({"ad": ["Ece", "Mert", "Zeynep", "Can", "Deniz"],
                       "vize": [60, 75, 40, 90, 55], "final": [70, 85, 55, 95, 42]})
notlar["ortalama"] = notlar["vize"] * 0.4 + notlar["final"] * 0.6
notlar["durum"] = "Kaldı"
notlar.loc[notlar["ortalama"] >= 50, "durum"] = "Geçti"
print(notlar.sort_values("ortalama", ascending=False).to_string(index=False))
print("Sınıf ortalaması:", notlar["ortalama"].mean().round(1))


# %% Alıştırma 3 — çözüm
import numpy as np
import pandas as pd

satis = np.array([[120, 135, 128, 150],
                  [ 98, 110, 105, 120],
                  [140, 138, 152, 160]])
df = pd.DataFrame(satis, index=["Kadıköy", "Bornova", "Çankaya"],
                  columns=["Oca", "Şub", "Mar", "Nis"])
df["Toplam"] = df.sum(axis=1)
print(df)
print("En çok satan:", df["Toplam"].idxmax())
print("Mart > 120:", df[df["Mar"] > 120].index.tolist())
