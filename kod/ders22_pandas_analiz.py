# =============================================================================
# Python Kursu — Ders 22 (Hafta 11, Gün 2)
# Konu: groupby ve agg, transform, map/apply, pivot_table, crosstab, stack/unstack, merge, concat, zamana göre gruplama, pct_change, çok sayfalı Excel raporu — üç aylık mağaza satışları
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum: python -m pip install pandas openpyxl
#   - ÖNCE Bölüm 0'ı bir kez çalıştırın: satislar_3ay.csv, urunler.csv ve hedefler.csv dosyalarını üretir.
#   - Satış verileri rastgele üretilmiş örnek verilerdir (Ağustos–Ekim 2026, 4 mağaza, 5 ürün).
# =============================================================================


# %% Bölüm 0 — Ders dosyalarını oluştur (bir kez çalıştırın)
import numpy as np
import pandas as pd

rng = np.random.default_rng(22)
urunler = pd.DataFrame({
    "Ürün": ["Defter", "Kalem", "Ajanda", "Çanta", "Matara"],
    "Kategori": ["Kırtasiye", "Kırtasiye", "Kırtasiye", "Aksesuar", "Aksesuar"],
    "Birim Fiyat": [45.0, 12.5, 220.0, 650.0, 180.0]})
ortalama_adet = {"Defter": 12, "Kalem": 30, "Ajanda": 3, "Çanta": 1.5, "Matara": 4}
magaza_carpani = {"Kadıköy": 1.2, "Bornova": 1.0, "Çankaya": 1.1, "Nilüfer": 0.8}
satirlar = []
for tarih in pd.date_range("2026-08-01", "2026-10-31", freq="D"):
    okul = 1.6 if tarih.month == 9 else 1.0               # Eylül: okul dönemi
    hafta_sonu = 1.3 if tarih.dayofweek >= 5 else 1.0
    for magaza, carpan in magaza_carpani.items():
        for urun, ort in ortalama_adet.items():
            etki = okul if urun in ("Defter", "Kalem", "Ajanda") else 1.0
            adet = int(rng.poisson(ort * carpan * etki * hafta_sonu))
            satirlar.append({"Tarih": tarih.date(), "Mağaza": magaza, "Ürün": urun, "Adet": adet})
pd.DataFrame(satirlar).to_csv("satislar_3ay.csv", index=False)
urunler.to_csv("urunler.csv", index=False)
pd.DataFrame({"Mağaza": list(magaza_carpani), "Aylık Hedef": [140000, 115000, 130000, 95000]}
             ).to_csv("hedefler.csv", index=False)
print(len(satirlar), "satış satırı yazıldı.")


# %% Bölüm 1 — Veriyi tanımak
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

print(df.shape)
print(df.head(3).to_string())
print(df["Tarih"].min().date(), "–", df["Tarih"].max().date())


# %% Bölüm 2 — groupby ile tek sütun özeti
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

print(df.groupby("Mağaza")["Ciro"].sum().sort_values(ascending=False))
print(df.groupby("Kategori")["Adet"].mean().round(1))


# %% Bölüm 3a — agg ile adlandırılmış özetler
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

ozet = df.groupby("Mağaza").agg(
    toplam_ciro=("Ciro", "sum"),
    ortalama_ciro=("Ciro", "mean"),
    satir_sayisi=("Ciro", "size"),
    satilan_adet=("Adet", "sum"),
).round(1)
print(ozet.sort_values("toplam_ciro", ascending=False))


# %% Bölüm 3b — agg ile fonksiyon listesi
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

print(df.groupby("Ürün")["Adet"].agg(["sum", "mean", "max"]).round(1))


# %% Bölüm 4 — İki sütunla gruplama ve reset_index
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

ik = df.groupby(["Mağaza", "Kategori"])["Ciro"].sum()
print(ik.head(4))
tablo = ik.reset_index()
print(tablo.head(4))
print(tablo.sort_values("Ciro", ascending=False).iloc[0].to_dict())


# %% Bölüm 5 — Her grubun en iyisi
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

en_iyi = df.sort_values("Ciro", ascending=False).groupby("Mağaza").head(1)
print(en_iyi[["Mağaza", "Tarih", "Ürün", "Ciro"]].to_string(index=False))
print(df.groupby("Mağaza")["Ciro"].idxmax().map(lambda i: df.loc[i, "Ürün"]).to_dict())


# %% Bölüm 6 — transform: grup sonucunu satırlara geri yaymak
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

df["Mağaza Payı %"] = (df["Ciro"] / df.groupby("Mağaza")["Ciro"].transform("sum") * 100).round(3)
df["Mağaza Ort."] = df.groupby("Mağaza")["Ciro"].transform("mean").round(1)
print(df[["Mağaza", "Ürün", "Ciro", "Mağaza Ort.", "Mağaza Payı %"]].head(4).to_string(index=False))
print(df.groupby("Mağaza")["Mağaza Payı %"].sum().round(1).to_dict())


# %% Bölüm 7 — map ve apply
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

bolge = {"Kadıköy": "Marmara", "Nilüfer": "Marmara",
         "Bornova": "Ege", "Çankaya": "İç Anadolu"}
df["Bölge"] = df["Mağaza"].map(bolge)
print(df.groupby("Bölge")["Ciro"].sum().to_dict())


def adet_sinifi(adet):
    if adet == 0:
        return "satış yok"
    return "yüksek" if adet >= 20 else "normal"


df["Adet Sınıfı"] = df["Adet"].apply(adet_sinifi)
print(df["Adet Sınıfı"].value_counts().to_dict())


# %% Bölüm 8 — pivot_table
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

pt = df.pivot_table(index="Mağaza", columns="Kategori", values="Ciro",
                    aggfunc="sum", margins=True, margins_name="Toplam")
print(pt.round(0))


# %% Bölüm 9 — crosstab ve hafta içi/sonu karşılaştırması
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

df["Gün Tipi"] = df["Tarih"].dt.dayofweek.map(lambda g: "Hafta sonu" if g >= 5 else "Hafta içi")
gunluk = df.groupby(["Tarih", "Gün Tipi"])["Ciro"].sum().reset_index()
print(gunluk.groupby("Gün Tipi")["Ciro"].mean().round(0).to_dict())
print(pd.crosstab(df["Mağaza"], df["Adet"] == 0, rownames=["Mağaza"], colnames=["Satış yok mu?"]))


# %% Bölüm 10 — unstack ve stack
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

uzun = df.groupby(["Mağaza", "Kategori"])["Ciro"].sum()
genis = uzun.unstack()               # iç seviye (Kategori) sütunlara
print(genis.round(0))
print(genis.stack().head(3).round(0))


# %% Bölüm 11 — merge: ortak sütunla birleştirme
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
print(satis.columns.tolist(), urunler.columns.tolist())
df = satis.merge(urunler, on="Ürün", how="left")
print(df.shape, df["Kategori"].isna().sum(), "eşleşmeyen")
yeni = pd.DataFrame({"Ürün": ["Defter", "Silgi"], "Adet": [3, 5]})
print(yeni.merge(urunler, on="Ürün", how="left"))
print(yeni.merge(urunler, on="Ürün", how="inner"))


# %% Bölüm 12 — Hedeflerle birleştirme ve aylık gerçekleşme
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

hedefler = pd.read_csv("hedefler.csv")
df["Ay"] = df["Tarih"].dt.to_period("M")
aylik = df.groupby(["Mağaza", "Ay"])["Ciro"].sum().reset_index()
aylik = aylik.merge(hedefler, on="Mağaza")
aylik["Gerçekleşme %"] = (aylik["Ciro"] / aylik["Aylık Hedef"] * 100).round(1)
print(aylik[aylik["Ay"] == "2026-10"].to_string(index=False))


# %% Bölüm 13 — concat: alt alta eklemek
import pandas as pd

magazalar = ["Kadıköy", "Bornova"]
ekim = pd.DataFrame({"Mağaza": magazalar, "Ciro": [120000, 90000]})
kasim = pd.DataFrame({"Mağaza": magazalar, "Ciro": [125000, 88000]})
ekim["Ay"], kasim["Ay"] = "Ekim", "Kasım"
iki_ay = pd.concat([ekim, kasim], ignore_index=True)
print(iki_ay)


# %% Bölüm 14 — Zamana göre gruplama, resample, pct_change
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

aylik = df.groupby(df["Tarih"].dt.to_period("M"))["Ciro"].sum()
print(aylik)
print((aylik.pct_change() * 100).round(1).tolist())
haftalik = df.set_index("Tarih")["Ciro"].resample("W").sum()
print("Haftalık en yüksek:", haftalik.idxmax().date(), haftalik.max())
kirtasiye = df[df["Kategori"] == "Kırtasiye"].groupby(df["Tarih"].dt.month)["Adet"].sum()
print("Kırtasiye adetleri (ay):", kirtasiye.to_dict())


# %% Uygulama — Çeyrek dönem raporu (4 sayfalı Excel)
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]
hedefler = pd.read_csv("hedefler.csv")
df["Ay"] = df["Tarih"].dt.to_period("M").astype(str)

magaza_ay = df.pivot_table(index="Mağaza", columns="Ay", values="Ciro", aggfunc="sum", margins=True,
                           margins_name="Toplam").round(0)
kategori = df.pivot_table(index="Kategori", columns="Ay", values="Ciro", aggfunc="sum").round(0)
gerceklesme = (df.groupby(["Mağaza", "Ay"])["Ciro"].sum().reset_index()
               .merge(hedefler, on="Mağaza")
               .assign(Gerceklesme=lambda t: (t["Ciro"] / t["Aylık Hedef"] * 100).round(1)))
urun_sirasi = (df.groupby("Ürün").agg(Adet=("Adet", "sum"), Ciro=("Ciro", "sum"))
               .sort_values("Ciro", ascending=False))

with pd.ExcelWriter("ceyrek_raporu.xlsx") as yazici:
    magaza_ay.to_excel(yazici, sheet_name="Mağaza x Ay")
    kategori.to_excel(yazici, sheet_name="Kategori x Ay")
    gerceklesme.to_excel(yazici, sheet_name="Hedef", index=False)
    urun_sirasi.to_excel(yazici, sheet_name="Ürünler")
print(magaza_ay)
print(gerceklesme.groupby("Ay")["Gerceklesme"].mean().round(1).to_dict())
print("En çok ciro yapan ürün:", urun_sirasi.index[0])
print("ceyrek_raporu.xlsx: 4 sayfa kaydedildi.")


# %% Alıştırma 1 — çözüm
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

ozet = df.groupby("Ürün").agg(
    toplam_adet=("Adet", "sum"),
    toplam_ciro=("Ciro", "sum"),
    ort_adet=("Adet", "mean"),
).round(1).sort_values("toplam_ciro", ascending=False)
print(ozet)


# %% Alıştırma 2 — çözüm
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

df["Gün Tipi"] = df["Tarih"].dt.dayofweek.map(lambda g: "Hafta sonu" if g >= 5 else "Hafta içi")
pt = df.pivot_table(index="Mağaza", columns="Gün Tipi", values="Ciro", aggfunc="sum")
pt["Hafta sonu %"] = (pt["Hafta sonu"] / pt.sum(axis=1) * 100).round(1)
print(pt.round(0))


# %% Alıştırma 3 — çözüm
import pandas as pd

satis = pd.read_csv("satislar_3ay.csv", parse_dates=["Tarih"])
urunler = pd.read_csv("urunler.csv")
df = satis.merge(urunler, on="Ürün")
df["Ciro"] = df["Adet"] * df["Birim Fiyat"]

hedefler = pd.read_csv("hedefler.csv")
df["Ay"] = df["Tarih"].dt.to_period("M").astype(str)
aylik = df.groupby(["Mağaza", "Ay"])["Ciro"].sum().reset_index()
en_iyi = aylik.sort_values("Ciro", ascending=False).groupby("Mağaza").head(1)
en_iyi = en_iyi.merge(hedefler, on="Mağaza", validate="one_to_one")
en_iyi["Gerçekleşme %"] = (en_iyi["Ciro"] / en_iyi["Aylık Hedef"] * 100).round(1)
en_iyi.to_csv("en_iyi_aylar.csv", index=False, encoding="utf-8-sig")
print(en_iyi.to_string(index=False))
