# =============================================================================
# Python Kursu — Ders 24 (Hafta 12, Gün 2)
# Konu: plot, özelleştirme, eksenler, fig/ax yapısı, scatter, histogram, bar/barh, gruplu ve yığılmış bar, stackplot, pie, subplots, Pandas ile çizim, kaydetme ve stiller — kişisel bütçe paneli
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Kurulum: python -m pip install matplotlib pandas
#   - Bazı örnekler Ders 23'te oluşturduğunuz ev_ilanlari_temiz.csv dosyasını kullanır; dosya bu .py ile aynı klasörde olmalı.
#   - VS Code'da hücreyi çalıştırınca grafik Interactive penceresinde görünür; terminalde çalıştırınca ayrı bir pencere açılır.
#   - Sıcaklık, satış ve harcama sayıları örnek (kurgusal) verilerdir.
# =============================================================================


# %% Bölüm 1 — Bir grafiğin parçaları
import matplotlib.pyplot as plt

gunler = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
istanbul = [14, 15, 13, 16, 18, 17, 15]
ankara = [8, 10, 7, 9, 12, 11, 9]
plt.figure(figsize=(8, 5))
plt.plot(gunler, istanbul, marker="o", label="İstanbul")
plt.plot(gunler, ankara, marker="s", label="Ankara")
plt.title("Haftalık en yüksek sıcaklık (örnek veri)")
plt.xlabel("Gün")
plt.ylabel("Sıcaklık (°C)")
plt.legend()
plt.grid(alpha=0.3)
plt.show()


# %% Bölüm 2 — İlk grafik
import matplotlib.pyplot as plt

gunler = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
istanbul = [14, 15, 13, 16, 18, 17, 15]
plt.plot(gunler, istanbul)
plt.show()


# %% Bölüm 3 — Çizgi stilleri
import matplotlib.pyplot as plt

gunler = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
istanbul = [14, 15, 13, 16, 18, 17, 15]
plt.figure(figsize=(8, 5))
plt.plot(gunler, istanbul, color="tomato", linewidth=3,
         linestyle="--", marker="o", markersize=10)
plt.title("İstanbul, bir hafta (örnek veri)")
plt.ylabel("°C")
plt.show()


# %% Bölüm 4 — İki çizgi, legend ve referans çizgisi
import matplotlib.pyplot as plt

gunler = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
istanbul = [14, 15, 13, 16, 18, 17, 15]
ankara = [8, 10, 7, 9, 12, 11, 9]
plt.figure(figsize=(8, 5))
plt.plot(gunler, istanbul, marker="o", label="İstanbul")
plt.plot(gunler, ankara, marker="s", label="Ankara")
plt.axhline(12, color="gray", linestyle=":", label="12 °C")
plt.legend(loc="upper left")
plt.show()


# %% Bölüm 5 — Eksen sınırları ve işaretler
import matplotlib.pyplot as plt

aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
market = [6200, 5900, 6400, 6100, 6800, 7000]
plt.figure(figsize=(8, 5))
plt.plot(aylar, market, marker="o")
plt.ylim(0, 8000)
plt.yticks(range(0, 8001, 2000))
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.4)
plt.title("Aylık market harcaması (TL, örnek)")
plt.show()


# %% Bölüm 6 — fig, ax = plt.subplots()
import matplotlib.pyplot as plt

aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
market = [6200, 5900, 6400, 6100, 6800, 7000]
eglence = [1200, 900, 1500, 1300, 2200, 2600]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(aylar, market, marker="o", label="Market")
ax.plot(aylar, eglence, marker="o", label="Eğlence")
ax.set_title("İki kalem (TL, örnek)")
ax.set_ylabel("TL")
ax.set_ylim(0, 8000)
ax.legend()
plt.show()


# %% Bölüm 7 — scatter: metrekare ve fiyat
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["metrekare"], df["fiyat"] / 1e6)
ax.set_xlabel("Metrekare")
ax.set_ylabel("Fiyat (milyon TL)")
ax.set_title("Metrekare ve fiyat (kurgusal ilanlar)")
plt.show()


# %% Bölüm 8 — scatter: ilçeye göre renk, odaya göre boyut
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
fig, ax = plt.subplots(figsize=(8, 5))
for ilce, grup in df.groupby("ilce"):
    ax.scatter(grup["metrekare"], grup["fiyat"] / 1e6,
               label=ilce, alpha=0.7, s=grup["oda_sayisi"] * 30)
ax.set_xlabel("Metrekare")
ax.set_ylabel("Fiyat (milyon TL)")
ax.legend(title="İlçe")
plt.show()


# %% Bölüm 9 — Histogram
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df["fiyat"] / 1e6, bins=12, color="steelblue",
        edgecolor="white")
ort = df["fiyat"].mean() / 1e6
ax.axvline(ort, color="tomato", linestyle="--",
           label=f"Ortalama: {ort:.1f} milyon")
ax.set_xlabel("Fiyat (milyon TL)")
ax.set_ylabel("İlan sayısı")
ax.legend()
plt.show()


# %% Bölüm 10 — bar: ilçelere göre m² fiyatı
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
medyan = df.groupby("ilce")["m2_fiyat"].median().sort_values()
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(medyan.index, medyan.values / 1000, color="steelblue")
ax.set_ylabel("Medyan m² fiyatı (bin TL)")
ax.set_title("İlçelere göre m² fiyatı (kurgusal)")
plt.show()


# %% Bölüm 11 — barh ve bar_label
import matplotlib.pyplot as plt

kalemler = {"Kira": 15000, "Market": 7000, "Eğlence": 2600,
            "Ulaşım": 1950, "Faturalar": 1450}
sirali = dict(sorted(kalemler.items(), key=lambda t: t[1]))
fig, ax = plt.subplots(figsize=(8, 5))
cubuklar = ax.barh(list(sirali), list(sirali.values()),
                   color="seagreen")
ax.bar_label(cubuklar, fmt="{:,.0f} TL", padding=4)
ax.set_xlim(0, 18000)
ax.set_title("Haziran harcamaları (örnek)")
plt.show()


# %% Bölüm 12 — Gruplu bar
import matplotlib.pyplot as plt
import numpy as np

ceyrek = ["1. Ç", "2. Ç", "3. Ç", "4. Ç"]
kadikoy = [420, 380, 510, 560]
bornova = [350, 400, 450, 470]
x = np.arange(len(ceyrek))
gen = 0.38
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - gen / 2, kadikoy, gen, label="Kadıköy")
ax.bar(x + gen / 2, bornova, gen, label="Bornova")
ax.set_xticks(x, ceyrek)
ax.set_ylabel("Satış (bin TL)")
ax.legend()
plt.show()


# %% Bölüm 13 — Yığılmış bar
import matplotlib.pyplot as plt
import numpy as np

aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
kalemler = {"Kira": [15000] * 6,
            "Market": [6200, 5900, 6400, 6100, 6800, 7000],
            "Ulaşım": [1800, 1750, 1900, 2000, 2100, 1950],
            "Eğlence": [1200, 900, 1500, 1300, 2200, 2600]}
fig, ax = plt.subplots(figsize=(8, 5))
alt = np.zeros(len(aylar))
for ad, tutar in kalemler.items():
    ax.bar(aylar, tutar, bottom=alt, label=ad)
    alt = alt + np.array(tutar)
ax.set_ylabel("TL")
ax.legend(ncols=4, loc="upper center")
ax.set_ylim(0, 32000)
plt.show()


# %% Bölüm 14 — stackplot
import matplotlib.pyplot as plt

aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
market = [6200, 5900, 6400, 6100, 6800, 7000]
ulasim = [1800, 1750, 1900, 2000, 2100, 1950]
eglence = [1200, 900, 1500, 1300, 2200, 2600]
fig, ax = plt.subplots(figsize=(8, 5))
ax.stackplot(aylar, market, ulasim, eglence,
             labels=["Market", "Ulaşım", "Eğlence"], alpha=0.85)
ax.set_title("Kira dışı harcamalar (TL, örnek)")
ax.legend(loc="upper left")
ax.set_ylim(0, 14000)
plt.show()


# %% Bölüm 15 — pie
import matplotlib.pyplot as plt

kalemler = ["Kira", "Market", "Eğlence", "Ulaşım", "Faturalar"]
tutarlar = [15000, 7000, 2600, 1950, 1450]
fig, ax = plt.subplots(figsize=(7, 6))
ax.pie(tutarlar, labels=kalemler, autopct="%1.0f%%",
       startangle=90, explode=[0.06, 0, 0, 0, 0],
       wedgeprops={"edgecolor": "white"})
ax.set_title("Haziran bütçesinin dağılımı (örnek)")
plt.show()


# %% Bölüm 16 — subplots
import matplotlib.pyplot as plt

aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
market = [6200, 5900, 6400, 6100, 6800, 7000]
eglence = [1200, 900, 1500, 1300, 2200, 2600]
fig, axs = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
axs[0].plot(aylar, market, marker="o")
axs[0].set_title("Market")
axs[1].bar(aylar, eglence, color="tomato")
axs[1].set_title("Eğlence")
fig.suptitle("İki kalem yan yana (TL, örnek)")
fig.tight_layout()
plt.show()


# %% Bölüm 17 — Pandas ile çizim
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
tablo = df.pivot_table(index="ilce", columns="oda",
                       values="fiyat", aggfunc="median") / 1e6
ax = tablo.plot(kind="bar", figsize=(8, 5), rot=0)
ax.set_ylabel("Medyan fiyat (milyon TL)")
ax.set_title("İlçe ve oda tipine göre (kurgusal)")
plt.show()


# %% Bölüm 18 — Stil ve kaydetme
import matplotlib.pyplot as plt

plt.style.use("ggplot")
aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
eglence = [1200, 900, 1500, 1300, 2200, 2600]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(aylar, eglence, marker="o", linewidth=3)
ax.set_title("Eğlence harcaması (TL, örnek)")
fig.savefig("eglence.png", dpi=150, bbox_inches="tight")
print("eglence.png kaydedildi")
plt.show()
plt.style.use("default")


# %% Uygulama — Kişisel bütçe paneli (2×2)
import matplotlib.pyplot as plt
import numpy as np

aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
kalemler = {"Kira": np.array([15000] * 6),
            "Market": np.array([6200, 5900, 6400, 6100, 6800, 7000]),
            "Ulaşım": np.array([1800, 1750, 1900, 2000, 2100, 1950]),
            "Eğlence": np.array([1200, 900, 1500, 1300, 2200, 2600])}
toplam = sum(kalemler.values())
gelir = 26000

fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# 1) Aylık toplam ve gelir çizgisi
axs[0, 0].plot(aylar, toplam, marker="o", linewidth=3, label="Toplam gider")
axs[0, 0].axhline(gelir, color="green", linestyle="--", label="Gelir")
axs[0, 0].set_ylim(0, 30000)
axs[0, 0].set_title("Toplam gider")
axs[0, 0].legend()

# 2) Kalemlere göre yığılmış bar
alt = np.zeros(len(aylar))
for ad, tutar in kalemler.items():
    axs[0, 1].bar(aylar, tutar, bottom=alt, label=ad)
    alt = alt + tutar
axs[0, 1].set_ylim(0, 32000)
axs[0, 1].set_title("Kalemlere göre")
axs[0, 1].legend(fontsize=9, ncols=2)

# 3) Son ayın dağılımı
son = {ad: tutar[-1] for ad, tutar in kalemler.items()}
axs[1, 0].pie(list(son.values()), labels=list(son), autopct="%1.0f%%", startangle=90)
axs[1, 0].set_title(f"{aylar[-1]} dağılımı")

# 4) Aylık birikim (gelir - gider)
birikim = gelir - toplam
renkler = ["seagreen" if b >= 0 else "tomato" for b in birikim]
cubuk = axs[1, 1].bar(aylar, birikim, color=renkler)
axs[1, 1].bar_label(cubuk, fmt="{:,.0f}")
axs[1, 1].axhline(0, color="black", linewidth=0.8)
axs[1, 1].set_title("Aylık birikim")

fig.suptitle("Kişisel bütçe paneli — Ocak–Haziran (örnek veri)", fontsize=16)
fig.tight_layout()
fig.savefig("butce_paneli.png", dpi=150)
plt.show()


# %% Alıştırma 1 — çözüm
import matplotlib.pyplot as plt

gunler = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
adimlar = [6500, 8200, 12000, 9100, 4300, 15000, 11000]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(gunler, adimlar, marker="o", label="Adım")
ax.axhline(10000, color="green", linestyle="--", label="Hedef")
ax.set_title("Haftalık adım sayısı")
ax.set_xlabel("Gün")
ax.set_ylabel("Adım")
ax.set_ylim(0, 16000)
ax.legend()
plt.show()


# %% Alıştırma 2 — çözüm
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)
notlar = rng.normal(68, 14, 30).clip(0, 100).round()
gecen = (notlar >= 50).sum()
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(notlar, bins=range(0, 101, 10), edgecolor="white")
ax.axvline(notlar.mean(), color="tomato",
           label=f"Ortalama: {notlar.mean():.1f}")
ax.axvline(50, color="black", linestyle="--", label="Geçme: 50")
ax.set_title(f"Not dağılımı — {gecen}/30 öğrenci geçti")
ax.set_xlabel("Not")
ax.set_ylabel("Öğrenci sayısı")
ax.legend()
plt.show()


# %% Alıştırma 3 — çözüm
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("ev_ilanlari_temiz.csv")
fig, axs = plt.subplots(1, 2, figsize=(12, 4.5))
sayilar = df["oda"].value_counts().sort_index()
axs[0].bar(sayilar.index, sayilar.values, color="slateblue")
axs[0].set_title("Oda tipine göre ilan sayısı")
axs[1].scatter(df["bina_yasi"], df["m2_fiyat"] / 1000, alpha=0.6)
axs[1].set_xlabel("Bina yaşı")
axs[1].set_ylabel("m² fiyatı (bin TL)")
axs[1].set_title("Bina yaşı ve m² fiyatı")
fig.tight_layout()
fig.savefig("ilan_panosu.png", dpi=150)
plt.show()
