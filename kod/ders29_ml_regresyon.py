# =============================================================================
# Python Kursu — Ders 29 (Hafta 15, Gün 1)
# Konu: Makine öğrenmesi kavramları, gözetimli/gözetimsiz öğrenme, regresyon ve sınıflandırma, scikit-learn fit/predict kalıbı, basit ve çoklu doğrusal regresyon, eğitim/test ayrımı, MAE/RMSE/R², kategorik özellikler, veri sızıntısı, Pipeline ve ColumnTransformer, çapraz doğrulama — ev fiyatı tahmini
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum: python -m pip install scikit-learn pandas matplotlib
#   - Ders 23'te oluşturduğunuz ev_ilanlari_temiz.csv bu .py ile aynı klasörde olmalı (ders29_veri klasöründe de var).
#   - İlanlar kurgusaldır; modelin sonuçları gerçek piyasa fiyatları hakkında bilgi vermez.
# =============================================================================


# %% Bölüm 1 — Veriye bakış
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

print(df.shape)
sutunlar = ["ilce", "metrekare", "oda_sayisi", "bina_yasi", "fiyat"]
print(df[sutunlar].head(4).to_string(index=False))
print(df[["metrekare", "fiyat"]].corr().round(2))


# %% Bölüm 2 — İlk model: fit
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.linear_model import LinearRegression

X = df[["metrekare"]]
y = df["fiyat"]
model = LinearRegression()
model.fit(X, y)
print("eğim:", round(model.coef_[0]), "TL / m²")
print("sabit:", round(model.intercept_), "TL")


# %% Bölüm 3 — Regresyon doğrusu
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

model = LinearRegression().fit(df[["metrekare"]], df["fiyat"])
x = pd.DataFrame({"metrekare": range(60, 181)})
plt.figure(figsize=(8, 5))
plt.scatter(df["metrekare"], df["fiyat"] / 1e6, alpha=0.5, label="ilanlar")
plt.plot(x["metrekare"], model.predict(x) / 1e6, color="tomato", linewidth=3,
         label="model")
plt.xlabel("Metrekare")
plt.ylabel("Fiyat (milyon TL)")
plt.legend()
plt.show()


# %% Bölüm 4 — Yeni evler için tahmin
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.linear_model import LinearRegression

model = LinearRegression().fit(df[["metrekare"]], df["fiyat"])
yeni = pd.DataFrame({"metrekare": [80, 120, 160]})
yeni["tahmin"] = model.predict(yeni[["metrekare"]]).round(-4)
print(yeni.to_string(index=False))


# %% Bölüm 5 — Eğitim/test ve metrikler
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

X, y = df[["metrekare"]], df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
tahmin = model.predict(X_test)
print(f"MAE : {mean_absolute_error(y_test, tahmin):,.0f} TL")
print(f"RMSE: {mean_squared_error(y_test, tahmin) ** 0.5:,.0f} TL")
print(f"R²  : {r2_score(y_test, tahmin):.2f}")


# %% Bölüm 6 — Çoklu regresyon (sayısal özellikler)
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

ozellikler = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
X, y = df[ozellikler], df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
tahmin = model.predict(X_test)
print(f"eğitim R²: {model.score(X_egitim, y_egitim):.2f}")
print(f"test R²  : {r2_score(y_test, tahmin):.2f}  ·  MAE: {mean_absolute_error(y_test, tahmin):,.0f} TL")


# %% Bölüm 7 — İlçe bilgisiyle (get_dummies)
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

ozellikler = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
X = pd.get_dummies(df[ozellikler + ["ilce"]], columns=["ilce"], drop_first=True, dtype=int)
y = df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
tahmin = model.predict(X_test)
print(X.columns.tolist())
print(f"test R²: {r2_score(y_test, tahmin):.2f}  ·  MAE: {mean_absolute_error(y_test, tahmin):,.0f} TL")


# %% Bölüm 7b — Modelleri karşılaştırma grafiği
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

import matplotlib.pyplot as plt

modeller = ["yalnızca\nmetrekare", "5 sayısal\nözellik", "+ ilçe"]
r2 = [0.41, 0.30, 0.93]
mae = [1.87, 1.96, 0.63]
fig, axs = plt.subplots(1, 2, figsize=(10, 4.5))
axs[0].bar(modeller, r2, color=["gray", "gray", "seagreen"])
axs[0].set_title("Test R² (yüksek iyi)")
axs[0].set_ylim(0, 1)
axs[1].bar(modeller, mae, color=["gray", "gray", "seagreen"])
axs[1].set_title("MAE, milyon TL (düşük iyi)")
fig.tight_layout()
plt.show()


# %% Bölüm 8 — Katsayıları yorumlamak
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

ozellikler = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
X = pd.get_dummies(df[ozellikler + ["ilce"]], columns=["ilce"], drop_first=True, dtype=int)
y = df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
tahmin = model.predict(X_test)

katsayi = pd.Series(model.coef_, index=X.columns).round(-3)
print(katsayi.to_string())


# %% Bölüm 9 — Tahmin ve gerçek grafiği
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

ozellikler = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
X = pd.get_dummies(df[ozellikler + ["ilce"]], columns=["ilce"], drop_first=True, dtype=int)
y = df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
tahmin = model.predict(X_test)

import matplotlib.pyplot as plt

plt.figure(figsize=(6.5, 6))
plt.scatter(y_test / 1e6, tahmin / 1e6, s=60, alpha=0.8)
plt.plot([1, 17], [1, 17], color="gray", linestyle="--", label="mükemmel tahmin")
plt.xlabel("Gerçek fiyat (milyon TL)")
plt.ylabel("Tahmin (milyon TL)")
plt.title("Test verisi: 26 ilan")
plt.legend()
plt.show()


# %% Bölüm 10 — Artıkların dağılımı
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

ozellikler = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
X = pd.get_dummies(df[ozellikler + ["ilce"]], columns=["ilce"], drop_first=True, dtype=int)
y = df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
tahmin = model.predict(X_test)

import matplotlib.pyplot as plt

artik = (y_test - tahmin) / 1e6
plt.figure(figsize=(6.5, 6))
plt.hist(artik, bins=10, edgecolor="white")
plt.axvline(0, color="tomato", linewidth=2)
plt.xlabel("Artık: gerçek − tahmin (milyon TL)")
plt.ylabel("İlan sayısı")
plt.title("Hataların dağılımı")
plt.show()


# %% Bölüm 11 — Veri sızıntısı örneği
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X = df[["metrekare", "m2_fiyat"]]
y = df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
print(f"test R²: {model.score(X_test, y_test):.3f}   ← şüpheli derecede iyi!")


# %% Bölüm 12 — Pipeline ve ColumnTransformer
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

sayisal = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
kategorik = ["ilce"]
hazirlik = ColumnTransformer([
    ("kategorik", OneHotEncoder(drop="first", handle_unknown="ignore"), kategorik),
    ("sayisal", "passthrough", sayisal),
])
pipe = make_pipeline(hazirlik, LinearRegression())

X, y = df[sayisal + kategorik], df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
pipe.fit(X_egitim, y_egitim)
print(f"test R²: {pipe.score(X_test, y_test):.2f}")


# %% Bölüm 13 — Çapraz doğrulama
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

sayisal = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
kategorik = ["ilce"]
hazirlik = ColumnTransformer([
    ("kategorik", OneHotEncoder(drop="first", handle_unknown="ignore"), kategorik),
    ("sayisal", "passthrough", sayisal),
])
pipe = make_pipeline(hazirlik, LinearRegression())

X, y = df[sayisal + kategorik], df["fiyat"]

from sklearn.model_selection import cross_val_score

skorlar = cross_val_score(pipe, X, y, cv=5, scoring="r2")
print("5 katlı R²:", skorlar.round(2))
print(f"ortalama: {skorlar.mean():.2f} ± {skorlar.std():.2f}")


# %% Uygulama — Modeli kaydet, yükle, yeni ilan tahmin et
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

sayisal = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
kategorik = ["ilce"]
hazirlik = ColumnTransformer([
    ("kategorik", OneHotEncoder(drop="first", handle_unknown="ignore"), kategorik),
    ("sayisal", "passthrough", sayisal),
])
pipe = make_pipeline(hazirlik, LinearRegression())

X, y = df[sayisal + kategorik], df["fiyat"]

import joblib
import pandas as pd

pipe.fit(X, y)                               # bütün veriyle son eğitim
joblib.dump(pipe, "ev_fiyat_modeli.joblib")

yuklenen = joblib.load("ev_fiyat_modeli.joblib")
yeni = pd.DataFrame([
    {"ilce": "Kadıköy", "metrekare": 110, "oda_sayisi": 3, "bina_yasi": 12, "kat": 4, "asansor": True},
    {"ilce": "Esenyurt", "metrekare": 110, "oda_sayisi": 3, "bina_yasi": 12, "kat": 4, "asansor": True},
])
yeni["tahmin"] = yuklenen.predict(yeni).round(-4)
print(yeni[["ilce", "metrekare", "tahmin"]].to_string(index=False))


# %% Alıştırma 1 — çözüm
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

X, y = df[["bina_yasi"]], df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
print(f"katsayı: {model.coef_[0]:,.0f} TL / yıl")
print(f"test R²: {model.score(X_test, y_test):.2f}")
print(f"MAE    : {mean_absolute_error(y_test, model.predict(X_test)):,.0f} TL")


# %% Alıştırma 2 — çözüm
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

sonuc = {}
for oz in ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]:
    hazirlik = ColumnTransformer([
        ("ilce", OneHotEncoder(drop="first"), ["ilce"]),
        ("sayi", "passthrough", [oz])])
    pipe = make_pipeline(hazirlik, LinearRegression())
    X = df[["ilce", oz]]
    sonuc[oz] = cross_val_score(pipe, X, df["fiyat"], cv=5).mean()
print(pd.Series(sonuc).sort_values(ascending=False).round(2).to_string())


# %% Alıştırma 3 — çözüm
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

ozellikler = ["metrekare", "oda_sayisi", "bina_yasi", "kat", "asansor"]
X = pd.get_dummies(df[ozellikler + ["ilce"]], columns=["ilce"], drop_first=True, dtype=int)
y = df["fiyat"]
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression().fit(X_egitim, y_egitim)
tahmin = model.predict(X_test)

sonuc = X_test.copy()
sonuc["ilce"] = df.loc[X_test.index, "ilce"]
sonuc["gercek"] = y_test
sonuc["tahmin"] = tahmin.round(-4)
sonuc["hata"] = (sonuc["gercek"] - sonuc["tahmin"]).abs()
print(sonuc.nlargest(5, "hata")[["ilce", "metrekare", "gercek", "tahmin", "hata"]].to_string(index=False))
print(sonuc.groupby("ilce")["hata"].mean().round(-3).sort_values().to_string())
