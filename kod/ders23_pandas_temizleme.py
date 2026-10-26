# =============================================================================
# Python Kursu — Ders 23 (Hafta 12, Gün 1)
# Konu: Veri keşfi, tekrarlar, metin temizliği, sayıya çevirme, eksik değer stratejileri, aykırı değerler, tip dönüşümleri, yeni özellikler, pd.cut, normalleştirme (min-max, z-skor), get_dummies — kirli ev ilanları veri seti
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum: python -m pip install pandas
#   - ÖNCE Bölüm 0'ı bir kez çalıştırın: ev_ilanlari_kirli.csv dosyasını üretir.
#   - İlanlar rastgele üretilmiş KURGUSAL verilerdir; ilçe adları gerçek, fiyatlar gerçek piyasayı yansıtmaz. Temizlenen dosya Ders 29'da (fiyat tahmini) kullanılacak.
# =============================================================================


# %% Bölüm 0 — Kirli veri setini oluştur (bir kez çalıştırın)
import numpy as np
import pandas as pd

rng = np.random.default_rng(23)
ilceler = {"Beşiktaş": 115000, "Kadıköy": 105000, "Üsküdar": 82000, "Maltepe": 68000, "Esenyurt": 34000}
satirlar = []
for no in range(1, 131):
    ilce = rng.choice(list(ilceler))
    oda = int(rng.choice([1, 2, 3, 4], p=[0.15, 0.4, 0.35, 0.1]))
    m2 = int(rng.normal(45 + oda * 28, 12))
    yas = int(rng.integers(0, 40))
    kat = int(rng.integers(-1, 12))
    asansor = "Var" if (kat > 3 or rng.random() < 0.5) else "Yok"
    fiyat = ilceler[ilce] * m2 * (1 - 0.008 * yas) * rng.normal(1, 0.08)
    fiyat = int(round(fiyat, -4))
    satirlar.append({"ilan_no": 1000 + no, "ilce": ilce, "oda": f"{oda}+1", "metrekare": m2,
                     "bina_yasi": yas, "kat": kat, "asansor": asansor,
                     "fiyat": f"{fiyat:,}".replace(",", ".") + " TL",
                     "ilan_tarihi": (pd.Timestamp("2026-09-01") + pd.Timedelta(days=int(rng.integers(0, 50)))).strftime("%Y-%m-%d")})
df = pd.DataFrame(satirlar)
# kirletme
yazim = {"Kadıköy": ["Kadıköy ", "kadıköy", "Kadikoy"], "Beşiktaş": ["BEŞİKTAŞ", "Besiktas"], "Üsküdar": [" Üsküdar"]}
for i in rng.choice(len(df), 18, replace=False):
    if df.loc[i, "ilce"] in yazim:
        df.loc[i, "ilce"] = rng.choice(yazim[df.loc[i, "ilce"]])
for i in rng.choice(len(df), 10, replace=False):
    df.loc[i, "oda"] = df.loc[i, "oda"].replace("+", " + ")
for i in rng.choice(len(df), 12, replace=False):
    df.loc[i, "asansor"] = rng.choice(["var", "VAR", "yok"])
df["metrekare"] = df["metrekare"].astype("float")
for i in rng.choice(len(df), 6, replace=False):
    df.loc[i, "metrekare"] = np.nan
df.loc[rng.choice(len(df), 2, replace=False), "metrekare"] = 9999.0
df["bina_yasi"] = df["bina_yasi"].astype("float")
for i in rng.choice(len(df), 5, replace=False):
    df.loc[i, "bina_yasi"] = np.nan
for i in rng.choice(len(df), 8, replace=False):
    df.loc[i, "fiyat"] = df.loc[i, "fiyat"].replace(" TL", "").replace(".", "")
for i in rng.choice(len(df), 4, replace=False):
    df.loc[i, "fiyat"] = ""
for i in rng.choice(len(df), 3, replace=False):
    df.loc[i, "asansor"] = ""
df = pd.concat([df, df.sample(5, random_state=1)], ignore_index=True)
df.to_csv("ev_ilanlari_kirli.csv", index=False)
print("ev_ilanlari_kirli.csv hazır:", df.shape)


# %% Bölüm 1 — İlk bakış
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")

print(df.shape)
print(df.head(5).to_string())


# %% Bölüm 2 — Keşif: tip, eksik, tekrar, kategori
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")

print(df.dtypes.astype(str).to_dict())
print("Eksikler:", df.isna().sum()[lambda s: s > 0].to_dict())
print("Tekrar eden satır:", df.duplicated().sum())
print(df["ilce"].value_counts().to_dict())
print(df["asansor"].value_counts(dropna=False).to_dict())


# %% Bölüm 3 — Tekrar eden satırlar
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")

print("Önce:", df.shape, "· tekrar:", df.duplicated().sum())
print("ilan_no tekrarı:", df["ilan_no"].duplicated().sum())
df = df.drop_duplicates()
print("Sonra:", df.shape)


# %% Bölüm 4 — Metin temizliği: ilçe adları
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

df = df.drop_duplicates().copy()

print(sorted(df["ilce"].unique().tolist()))
duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
print(df["ilce"].value_counts().to_dict())


# %% Bölüm 5 — Biçim birliği: oda ve asansör
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")

df = df.drop_duplicates().copy()

print(df["oda"].unique().tolist())
df["oda"] = df["oda"].str.replace(" ", "")
df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
print(df["oda"].value_counts().to_dict())
print(df["asansor"].value_counts(dropna=False).to_dict())


# %% Bölüm 6 — Metinden sayıya: fiyat
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")

df = df.drop_duplicates().copy()

print(df["fiyat"].head(4).tolist())
temiz = df["fiyat"].str.replace(" TL", "").str.replace(".", "")
df["fiyat"] = pd.to_numeric(temiz, errors="coerce")
print(df["fiyat"].dtype, "· eksik:", df["fiyat"].isna().sum())
print(df["fiyat"].describe().round(0).to_dict())


# %% Bölüm 7 — Eksik değerleri işlemek
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

df = df.drop_duplicates().copy()
duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
df["oda"] = df["oda"].str.replace(" ", "")
df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""), errors="coerce")

print("Önce:", df.isna().sum()[lambda s: s > 0].to_dict())
df = df.dropna(subset=["fiyat"])
oda_medyan = df.groupby("oda")["metrekare"].transform("median")
df["metrekare"] = df["metrekare"].fillna(oda_medyan)
df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median())
df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0])
print("Sonra:", df.isna().sum().sum(), "eksik ·", df.shape)


# %% Bölüm 8 — Aykırı değerler: IQR yöntemi
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")

df = df.drop_duplicates().copy()

print(df["metrekare"].describe()[["min", "50%", "max"]].to_dict())
q1, q3 = df["metrekare"].quantile([0.25, 0.75])
iqr = q3 - q1
alt, ust = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(f"IQR sınırları: {alt:.0f} – {ust:.0f}")
aykiri = (df["metrekare"] < alt) | (df["metrekare"] > ust)
print(df.loc[aykiri, ["ilan_no", "oda", "metrekare"]].to_string(index=False))
df.loc[aykiri, "metrekare"] = pd.NA


# %% Bölüm 9 — Tip dönüşümleri
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

df = df.drop_duplicates().copy()
duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
df["oda"] = df["oda"].str.replace(" ", "")
df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""), errors="coerce")
df = df.dropna(subset=["fiyat"])
df.loc[df["metrekare"] > 1000, "metrekare"] = pd.NA
df["metrekare"] = df["metrekare"].fillna(df.groupby("oda")["metrekare"].transform("median"))
df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median())
df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0]).astype(bool)

df["ilan_tarihi"] = pd.to_datetime(df["ilan_tarihi"])
df["ilce"] = df["ilce"].astype("category")
df["bina_yasi"] = df["bina_yasi"].astype(int)
print(df.dtypes.astype(str).to_dict())
print(df["ilce"].cat.categories.tolist())


# %% Bölüm 10 — Yeni özellikler türetmek
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

df = df.drop_duplicates().copy()
duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
df["oda"] = df["oda"].str.replace(" ", "")
df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""), errors="coerce")
df = df.dropna(subset=["fiyat"])
df.loc[df["metrekare"] > 1000, "metrekare"] = pd.NA
df["metrekare"] = df["metrekare"].fillna(df.groupby("oda")["metrekare"].transform("median"))
df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median())
df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0]).astype(bool)

df["oda_sayisi"] = df["oda"].str.split("+").str[0].astype(int)
df["m2_fiyat"] = (df["fiyat"] / df["metrekare"]).round(0)
df["ilan_gunu"] = (pd.Timestamp("2026-10-31") - pd.to_datetime(df["ilan_tarihi"])).dt.days
df["bodrum"] = df["kat"] < 0
print(df[["oda", "oda_sayisi", "m2_fiyat", "ilan_gunu", "bodrum"]].head(4).to_string(index=False))
print(df.groupby("ilce")["m2_fiyat"].median().sort_values(ascending=False).to_dict())


# %% Bölüm 11 — pd.cut ve pd.qcut
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

df = df.drop_duplicates().copy()
duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
df["oda"] = df["oda"].str.replace(" ", "")
df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""), errors="coerce")
df = df.dropna(subset=["fiyat"])
df.loc[df["metrekare"] > 1000, "metrekare"] = pd.NA
df["metrekare"] = df["metrekare"].fillna(df.groupby("oda")["metrekare"].transform("median"))
df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median())
df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0]).astype(bool)

df["yas_grubu"] = pd.cut(df["bina_yasi"], bins=[-1, 5, 15, 30, 100],
                         labels=["Yeni (0-5)", "Genç (6-15)", "Orta (16-30)", "Eski (31+)"])
print(df["yas_grubu"].value_counts().sort_index().to_dict())
df["fiyat_dilimi"] = pd.qcut(df["fiyat"], q=3, labels=["ucuz", "orta", "pahalı"])
print(df.groupby("fiyat_dilimi", observed=True)["fiyat"].agg(["min", "max"]).round(-4))


# %% Bölüm 12 — Min-max ve z-skor
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

df = df.drop_duplicates().copy()
duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
df["oda"] = df["oda"].str.replace(" ", "")
df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""), errors="coerce")
df = df.dropna(subset=["fiyat"])
df.loc[df["metrekare"] > 1000, "metrekare"] = pd.NA
df["metrekare"] = df["metrekare"].fillna(df.groupby("oda")["metrekare"].transform("median"))
df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median())
df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0]).astype(bool)

df["oda_sayisi"] = df["oda"].str.split("+").str[0].astype(int)
sutunlar = ["metrekare", "bina_yasi", "oda_sayisi"]
enk, enb = df[sutunlar].min(), df[sutunlar].max()
minmax = (df[sutunlar] - enk) / (enb - enk)
zskor = (df[sutunlar] - df[sutunlar].mean()) / df[sutunlar].std()
print(minmax.describe().loc[["min", "max"]].round(2))
print(zskor.describe().loc[["mean", "std"]].round(2))


# %% Bölüm 13 — get_dummies: kategorileri 0/1 sütunlarına çevirmek
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

df = df.drop_duplicates().copy()
duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
df["oda"] = df["oda"].str.replace(" ", "")
df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""), errors="coerce")
df = df.dropna(subset=["fiyat"])
df.loc[df["metrekare"] > 1000, "metrekare"] = pd.NA
df["metrekare"] = df["metrekare"].fillna(df.groupby("oda")["metrekare"].transform("median"))
df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median())
df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0]).astype(bool)

kodlu = pd.get_dummies(df[["ilce", "asansor", "metrekare"]], columns=["ilce"], prefix="ilce", dtype=int)
print(kodlu.head(3).to_string())
kodlu2 = pd.get_dummies(df["ilce"], prefix="ilce", drop_first=True, dtype=int)
print(kodlu2.columns.tolist())


# %% Bölüm 14 — Sıralı kategoriler: map ile kodlama
import pandas as pd

df = pd.read_csv("ev_ilanlari_kirli.csv")


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()

df = df.drop_duplicates().copy()
duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
df["oda"] = df["oda"].str.replace(" ", "")
df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""), errors="coerce")
df = df.dropna(subset=["fiyat"])
df.loc[df["metrekare"] > 1000, "metrekare"] = pd.NA
df["metrekare"] = df["metrekare"].fillna(df.groupby("oda")["metrekare"].transform("median"))
df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median())
df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0]).astype(bool)

sira = {"Yeni (0-5)": 0, "Genç (6-15)": 1,
        "Orta (16-30)": 2, "Eski (31+)": 3}
sinirlar = [-1, 5, 15, 30, 100]
df["yas_grubu"] = pd.cut(df["bina_yasi"], sinirlar, labels=list(sira))
df["yas_kodu"] = df["yas_grubu"].map(sira).astype(int)
ornek = df.drop_duplicates("yas_grubu").sort_values("yas_kodu")
print(ornek[["bina_yasi", "yas_grubu", "yas_kodu"]].to_string(index=False))


# %% Uygulama — temizle() fonksiyonu ve ev_ilanlari_temiz.csv
import pandas as pd


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()


def temizle(df):
    """Kirli ilan tablosunu analiz ve modele hazır hale getirir."""
    df = df.drop_duplicates().copy()
    duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
    df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
    df["oda"] = df["oda"].str.replace(" ", "")
    df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
    df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""),
                                errors="coerce")
    df = df.dropna(subset=["fiyat"])
    df.loc[df["metrekare"] > 1000, "metrekare"] = pd.NA            # aykırı → eksik
    df["metrekare"] = df["metrekare"].fillna(df.groupby("oda")["metrekare"].transform("median"))
    df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median()).astype(int)
    df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0]).astype(bool)
    df["ilan_tarihi"] = pd.to_datetime(df["ilan_tarihi"])
    df["oda_sayisi"] = df["oda"].str.split("+").str[0].astype(int)
    df["m2_fiyat"] = (df["fiyat"] / df["metrekare"]).round(0)
    return df.reset_index(drop=True)


ham = pd.read_csv("ev_ilanlari_kirli.csv")
temiz = temizle(ham)
print("Ham:", ham.shape, "· eksik:", ham.isna().sum().sum(), "· tekrar:", ham.duplicated().sum())
print("Temiz:", temiz.shape, "· eksik:", temiz.isna().sum().sum(), "· tekrar:", temiz.duplicated().sum())
print(temiz["ilce"].value_counts().to_dict())
print(temiz[["metrekare", "fiyat", "m2_fiyat"]].describe().loc[["min", "max"]].round(0))
temiz.to_csv("ev_ilanlari_temiz.csv", index=False)
print("ev_ilanlari_temiz.csv kaydedildi (Ders 29'da kullanılacak).")


# %% Alıştırma 1 — çözüm
import pandas as pd


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()


kat = pd.Series(["Market", "market ", "MARKET", "Ulaşım", "ulasim", None])
temiz = kat.str.strip().map(tr_kucuk, na_action="ignore").replace({"ulasim": "ulaşım"})
temiz = temiz.str.capitalize().fillna("Diğer")
print(temiz.value_counts().to_dict())


# %% Alıştırma 2 — çözüm
import pandas as pd

fiyat = pd.Series(["1.250,50 TL", "980 TL", "2.100,00", "yok"])
temiz = (fiyat.str.replace(" TL", "", regex=False)
              .str.replace(".", "", regex=False)
              .str.replace(",", ".", regex=False))
sayi = pd.to_numeric(temiz, errors="coerce")
print(sayi.tolist())
print("Çevrilemeyen:", sayi.isna().sum(), "· ortalama:", round(sayi.mean(), 2))


# %% Alıştırma 3 — çözüm
import pandas as pd


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()


def temizle(df):
    """Kirli ilan tablosunu analiz ve modele hazır hale getirir."""
    df = df.drop_duplicates().copy()
    duzelt = {"kadikoy": "kadıköy", "besiktas": "beşiktaş"}
    df["ilce"] = df["ilce"].str.strip().map(tr_kucuk).replace(duzelt).str.capitalize()
    df["oda"] = df["oda"].str.replace(" ", "")
    df["asansor"] = df["asansor"].str.strip().str.lower().map({"var": True, "yok": False})
    df["fiyat"] = pd.to_numeric(df["fiyat"].str.replace(" TL", "").str.replace(".", ""),
                                errors="coerce")
    df = df.dropna(subset=["fiyat"])
    df.loc[df["metrekare"] > 1000, "metrekare"] = pd.NA            # aykırı → eksik
    df["metrekare"] = df["metrekare"].fillna(df.groupby("oda")["metrekare"].transform("median"))
    df["bina_yasi"] = df["bina_yasi"].fillna(df["bina_yasi"].median()).astype(int)
    df["asansor"] = df["asansor"].fillna(df["asansor"].mode()[0]).astype(bool)
    df["ilan_tarihi"] = pd.to_datetime(df["ilan_tarihi"])
    df["oda_sayisi"] = df["oda"].str.split("+").str[0].astype(int)
    df["m2_fiyat"] = (df["fiyat"] / df["metrekare"]).round(0)
    return df.reset_index(drop=True)


df = temizle(pd.read_csv("ev_ilanlari_kirli.csv"))
df["kat_grubu"] = pd.cut(df["kat"], bins=[-2, -1, 0, 5, 100], labels=["bodrum", "giriş", "ara", "yüksek"])
print(df["kat_grubu"].value_counts().sort_index().to_dict())
print(df.groupby("ilce")["fiyat"].median().sort_values(ascending=False).round(-4).to_dict())
model_tablosu = pd.get_dummies(df[["ilce"]], prefix="ilce", drop_first=True, dtype=int)
model_tablosu["metrekare_z"] = ((df["metrekare"] - df["metrekare"].mean()) / df["metrekare"].std()).round(2)
print(model_tablosu.head(3).to_string())
