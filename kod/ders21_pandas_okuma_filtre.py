# =============================================================================
# Python Kursu — Ders 21 (Hafta 11, Gün 1)
# Konu: read_csv (sep, decimal, encoding, tarih), read_excel, read_sql (SQLite), to_csv/to_excel, açık veri portalları; filtreleme: koşullar, isin, between, str.contains, query, loc, nlargest — mağaza satış dosyası
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum: python -m pip install pandas openpyxl  (openpyxl Excel dosyaları için)
#   - ÖNCE Bölüm 0'ı bir kez çalıştırın: ders dosyalarını (magaza_satislari.csv, sube_bilgileri.xlsx, kutuphane.db, eski_kayitlar.csv) çalışma klasörüne oluşturur. Sonraki hücreler bu dosyaları okur.
#   - Dosyalardaki satış verileri rastgele üretilmiş örnek verilerdir; kitap bilgileri Ders 14'teki gibidir.
# =============================================================================


# %% Bölüm 0 — Ders dosyalarını oluştur (bir kez çalıştırın)
import sqlite3

import numpy as np
import pandas as pd

rng = np.random.default_rng(21)
tarihler = pd.date_range("2026-10-01", periods=8, freq="D")
magazalar = ["Kadıköy", "Bornova", "Çankaya"]
urunler = {"Defter": 45.0, "Kalem": 12.5, "Çanta": 650.0}
satirlar = []
for t in tarihler:
    for m in magazalar:
        for u, f in urunler.items():
            ust = 4 if u == "Çanta" else 30
            satirlar.append({"Tarih": t.strftime("%d.%m.%Y"), "Mağaza": m, "Ürün": u,
                             "Adet": int(rng.integers(0, ust)), "Birim Fiyat": f})
pd.DataFrame(satirlar).to_csv("magaza_satislari.csv", sep=";", decimal=",", index=False)

with pd.ExcelWriter("sube_bilgileri.xlsx") as yazici:
    pd.DataFrame({"Mağaza": magazalar, "Şehir": ["İstanbul", "İzmir", "Ankara"],
                  "Açılış Yılı": [2015, 2019, 2021], "Metrekare": [180, 140, 210]}
                 ).to_excel(yazici, sheet_name="Şubeler", index=False)
    pd.DataFrame({"Mağaza": magazalar, "Ekim Hedefi": [65000, 60000, 55000]}
                 ).to_excel(yazici, sheet_name="Hedefler", index=False)

kitaplar = [("Tutunamayanlar", "Oğuz Atay", 1972, 5), ("İnce Memed", "Yaşar Kemal", 1955, 4),
            ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
            ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
            ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
            ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3), ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
            ("Semaver", "Sait Faik Abasıyanık", 1936, 3)]
with sqlite3.connect("kutuphane.db") as baglanti:
    baglanti.execute("DROP TABLE IF EXISTS kitaplar")
    baglanti.execute("CREATE TABLE kitaplar (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                     "ad TEXT NOT NULL, yazar TEXT NOT NULL, yil INTEGER, puan INTEGER)")
    baglanti.executemany("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)", kitaplar)
baglanti.close()

with open("eski_kayitlar.csv", "w", encoding="cp1254") as f:
    f.write("Şehir;Şube Sayısı\nİstanbul;12\nİzmir;5\nAnkara;7\n")
print("Ders dosyaları hazır.")


# %% Ödev kontrolü — Film tablosu (kısa örnek)
import pandas as pd

filmler = pd.DataFrame({
    "ad": ["Eşkıya", "Babam ve Oğlum", "Kış Uykusu", "Ahlat Ağacı"],
    "yonetmen": ["Yavuz Turgul", "Çağan Irmak", "Nuri Bilge Ceylan", "Nuri Bilge Ceylan"],
    "yil": [1996, 2005, 2014, 2018]})
filmler["yas"] = 2026 - filmler["yil"]
print(filmler["yonetmen"].value_counts().to_dict())
filmler.to_csv("filmler.csv", index=False)


# %% Bölüm 1 — CSV dosyasının içi (düz metin)
with open("magaza_satislari.csv", encoding="utf-8") as f:
    for _ in range(4):
        print(f.readline().rstrip())


# %% Bölüm 2 — Varsayılan ayarla okuma (yanlış)
import pandas as pd

df = pd.read_csv("magaza_satislari.csv")
print(df.shape)
print(df.columns.tolist())


# %% Bölüm 3 — Doğru ayarlarla okuma
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
print(df.shape)
print(df.head(4))
print(df.dtypes.astype(str).to_dict())


# %% Bölüm 4 — Kodlama sorunu ve encoding
import pandas as pd

try:
    eski = pd.read_csv("eski_kayitlar.csv", sep=";")
except UnicodeDecodeError as hata:
    print("Hata:", hata)
eski = pd.read_csv("eski_kayitlar.csv", sep=";", encoding="cp1254")
print(eski)


# %% Bölüm 5 — read_excel ve sayfalar
import pandas as pd

print(pd.ExcelFile("sube_bilgileri.xlsx").sheet_names)
subeler = pd.read_excel("sube_bilgileri.xlsx", sheet_name="Şubeler")
print(subeler)
hepsi = pd.read_excel("sube_bilgileri.xlsx", sheet_name=None)
print(type(hepsi), list(hepsi))
print(hepsi["Hedefler"])


# %% Bölüm 6 — SQLite'tan read_sql
import sqlite3
import pandas as pd

baglanti = sqlite3.connect("kutuphane.db")
kitaplar = pd.read_sql("SELECT ad, yazar, yil, puan FROM kitaplar WHERE puan >= 4", baglanti)
baglanti.close()
print(kitaplar)
print(kitaplar["yil"].mean())


# %% Bölüm 7 — to_csv ve to_excel
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

kadikoy = df[df["Mağaza"] == "Kadıköy"]
kadikoy.to_csv("kadikoy.csv", sep=";", decimal=",", index=False, encoding="utf-8-sig")
with pd.ExcelWriter("rapor.xlsx") as yazici:
    kadikoy.to_excel(yazici, sheet_name="Kadıköy", index=False)
    df.describe().to_excel(yazici, sheet_name="Özet")
print(pd.read_excel("rapor.xlsx", sheet_name=None).keys())


# %% Bölüm 8 — Koşullu filtre tekrarı
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

print(df.shape)
canta = df[df["Ürün"] == "Çanta"]
print(len(canta), "çanta satırı · toplam adet:", canta["Adet"].sum())
buyuk = df[(df["Mağaza"] == "Kadıköy") & (df["Ciro"] >= 1000)]
print(buyuk[["Tarih", "Ürün", "Adet", "Ciro"]])


# %% Bölüm 9 — isin
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

secili = df[df["Mağaza"].isin(["Kadıköy", "Çankaya"]) & df["Ürün"].isin(["Defter", "Kalem"])]
print(secili.shape, secili["Mağaza"].unique().tolist())
print(df[~df["Ürün"].isin(["Çanta"])]["Ürün"].value_counts().to_dict())


# %% Bölüm 10 — between ve tarih filtreleri
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

print(df[df["Adet"].between(10, 15)].shape[0], "satırda adet 10–15 arası")
ilk_uc_gun = df[df["Tarih"].between("2026-10-01", "2026-10-03")]
print(ilk_uc_gun["Tarih"].dt.strftime("%d.%m").unique().tolist())
hafta_sonu = df[df["Tarih"].dt.dayofweek >= 5]
print(hafta_sonu["Tarih"].dt.strftime("%d.%m").unique().tolist(), hafta_sonu["Ciro"].sum())


# %% Bölüm 11 — str metotları ve Türkçe harfler
import pandas as pd

kitaplar = pd.DataFrame({
    "ad": ["İnce Memed", "Kürk Mantolu Madonna", "Saatleri Ayarlama Enstitüsü", "Semaver"],
    "yazar": ["Yaşar Kemal", "Sabahattin Ali", "Ahmet Hamdi Tanpınar", "Sait Faik Abasıyanık"]})
print(kitaplar[kitaplar["ad"].str.contains("Ma")]["ad"].tolist())
print(kitaplar[kitaplar["ad"].str.startswith("S")]["ad"].tolist())
print(kitaplar["ad"].str.contains("ince", case=False).tolist())          # İ sorunu!
kucuk = kitaplar["ad"].str.replace("İ", "i").str.replace("I", "ı").str.lower()
print(kitaplar[kucuk.str.contains("ince")]["ad"].tolist())


# %% Bölüm 12 — query
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

sonuc = df.query("Mağaza == 'Bornova' and Adet >= 20")
print(sonuc[["Tarih", "Ürün", "Adet"]])
esik = 600
print(df.query("`Birim Fiyat` > @esik")["Ürün"].unique().tolist())


# %% Bölüm 13 — loc ile seçip güncellemek, nlargest
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

print(df.loc[df["Ürün"] == "Çanta", ["Tarih", "Mağaza", "Adet"]].head(3))
df.loc[df["Adet"] == 0, "Not"] = "satış yok"
print(df["Not"].value_counts(dropna=False).to_dict())
print(df.nlargest(3, "Ciro")[["Tarih", "Mağaza", "Ürün", "Ciro"]])


# %% Uygulama — Haftalık satış raporu (CSV + Excel → filtre → Excel)
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

hedefler = pd.read_excel("sube_bilgileri.xlsx", sheet_name="Hedefler")
hafta = df[df["Tarih"].between("2026-10-01", "2026-10-07")]
print("Haftalık ciro:", hafta["Ciro"].sum(), "TL")
for magaza, hedef in zip(hedefler["Mağaza"], hedefler["Ekim Hedefi"]):
    ciro = hafta.loc[hafta["Mağaza"] == magaza, "Ciro"].sum()
    print(f"  {magaza:<8}{ciro:>9.1f} TL · Ekim hedefinin %{ciro / hedef * 100:.0f}’i")
canta_hs = hafta.query("Ürün == 'Çanta' and Tarih.dt.dayofweek >= 5 and Adet > 0")
print("Hafta sonu çanta satışları:")
print(canta_hs[["Tarih", "Mağaza", "Adet", "Ciro"]].to_string(index=False))
with pd.ExcelWriter("haftalik_rapor.xlsx") as yazici:
    hafta.to_excel(yazici, sheet_name="Satışlar", index=False)
    canta_hs.to_excel(yazici, sheet_name="Hafta sonu çanta", index=False)
print("haftalik_rapor.xlsx kaydedildi.")


# %% Alıştırma 1 — çözüm
import pandas as pd

subeler = pd.read_excel("sube_bilgileri.xlsx", sheet_name="Şubeler")
secili = subeler[(subeler["Açılış Yılı"] > 2018) & (subeler["Metrekare"] > 150)]
print(secili)
print(subeler.query("`Açılış Yılı` > 2018 and Metrekare > 150")["Mağaza"].tolist())


# %% Alıştırma 2 — çözüm
import pandas as pd

df = pd.read_csv("magaza_satislari.csv", sep=";", decimal=",",
                 parse_dates=["Tarih"], date_format="%d.%m.%Y")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

kalem = df[df["Ürün"] == "Kalem"]
print("Toplam adet:", kalem["Adet"].sum())
print(kalem.loc[kalem["Adet"] > 20, ["Tarih", "Mağaza", "Adet"]].to_string(index=False))
iki = kalem[kalem["Mağaza"].isin(["Bornova", "Çankaya"])]
print("Bornova + Çankaya kalem cirosu:", iki["Ciro"].sum())


# %% Alıştırma 3 — çözüm
import sqlite3
import pandas as pd

with sqlite3.connect("kutuphane.db") as baglanti:
    kitaplar = pd.read_sql("SELECT ad, yazar, yil, puan FROM kitaplar", baglanti)
kucuk = kitaplar["ad"].str.replace("İ", "i").str.replace("I", "ı").str.lower()
rapor = kitaplar[kucuk.str.contains("a") & (kitaplar["yil"] < 1950)]
rapor.to_csv("kitaplar_rapor.csv", index=False, encoding="utf-8-sig")
print(rapor)
