# =============================================================================
# Python Kursu — Ders 14 (Hafta 7, Gün 2)
# Konu: Veri tabanı ve SQL kavramları, sqlite3 modülü, CREATE TABLE, INSERT, SELECT, DB Browser for SQLite — kitap kayıtları
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - sqlite3 modülü Python ile gelir; kurulum gerekmez.
#   - Örnekler çalıştırıldığı klasörde kutuphane.db, kitaplik.db, harcamalar.db ve filmler.db dosyaları oluşturur.
#   - Bu dosyaları DB Browser for SQLite ile açıp inceleyebilirsiniz (sqlitebrowser.org).
# =============================================================================


# %% Bölüm 1 — Bağlantı ve imleç
import sqlite3

baglanti = sqlite3.connect("kutuphane.db")  # dosya yoksa oluşturur
imlec = baglanti.cursor()
imlec.execute("SELECT sqlite_version()")
print("SQLite sürümü:", imlec.fetchone()[0])
baglanti.close()


# %% Bölüm 2 — CREATE TABLE
import sqlite3

baglanti = sqlite3.connect("kutuphane.db")
imlec = baglanti.cursor()
imlec.execute("""
CREATE TABLE IF NOT EXISTS kitaplar (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    ad    TEXT NOT NULL,
    yazar TEXT NOT NULL,
    yil   INTEGER,
    puan  INTEGER DEFAULT 3
)""")
baglanti.commit()
print("Tablo hazır.")
baglanti.close()


# %% Bölüm 3 — INSERT ile tek kayıt
import sqlite3

baglanti = sqlite3.connect("kutuphane.db")
imlec = baglanti.cursor()
imlec.execute("""CREATE TABLE IF NOT EXISTS kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL,
    yazar TEXT NOT NULL, yil INTEGER, puan INTEGER DEFAULT 3)""")
imlec.execute("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)",
              ("Tutunamayanlar", "Oğuz Atay", 1972, 5))
baglanti.commit()
print("Eklenen kaydın id’si:", imlec.lastrowid)
baglanti.close()


# %% Bölüm 4 — f-string ile SQL (hatalı, satır yorumda) ve ? ile doğru yazım
import sqlite3

baglanti = sqlite3.connect(":memory:")  # bellekte geçici veri tabanı
baglanti.execute("CREATE TABLE kitaplar (ad TEXT, yazar TEXT)")
ad, yazar = "Ali'nin Hikâyesi", "Ayşe"
# baglanti.execute(f"INSERT INTO kitaplar VALUES ('{ad}', '{yazar}')")
# Hata: sqlite3.OperationalError: near "nin": syntax error

# Doğrusu:
baglanti.execute("INSERT INTO kitaplar VALUES (?, ?)", (ad, yazar))
print(baglanti.execute("SELECT * FROM kitaplar").fetchall())


# %% Bölüm 5 — executemany ile toplu ekleme
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
]
baglanti = sqlite3.connect("kutuphane.db")
imlec = baglanti.cursor()
imlec.execute("""CREATE TABLE IF NOT EXISTS kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL,
    yazar TEXT NOT NULL, yil INTEGER, puan INTEGER DEFAULT 3)""")
imlec.executemany("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)",
                  KITAPLAR[1:])
baglanti.commit()
print(imlec.rowcount, "kitap eklendi.")
baglanti.close()


# %% Bölüm 6 — with baglanti: otomatik commit
import sqlite3

baglanti = sqlite3.connect("kutuphane.db")
baglanti.execute("""CREATE TABLE IF NOT EXISTS kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL,
    yazar TEXT NOT NULL, yil INTEGER, puan INTEGER DEFAULT 3)""")
with baglanti:  # blok hatasız biterse otomatik commit
    baglanti.execute("INSERT INTO kitaplar (ad, yazar, yil) VALUES (?, ?, ?)",
                     ("Semaver", "Sait Faik Abasıyanık", 1936))
sayi = baglanti.execute("SELECT COUNT(*) FROM kitaplar").fetchone()[0]
print("Toplam kitap:", sayi)
baglanti.close()


# %% Bölüm 7 — SELECT * ve fetchall
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
]
baglanti = sqlite3.connect("kutuphane.db")
imlec = baglanti.cursor()
imlec.execute("DROP TABLE IF EXISTS kitaplar")  # örneği her seferinde temiz başlat
imlec.execute("""CREATE TABLE kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    yazar TEXT NOT NULL,
    yil INTEGER,
    puan INTEGER DEFAULT 3)""")
imlec.executemany("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)", KITAPLAR)
baglanti.commit()

imlec.execute("SELECT * FROM kitaplar")
satirlar = imlec.fetchall()
print(type(satirlar), len(satirlar))
for satir in satirlar[:3]:
    print(satir)
baglanti.close()


# %% Bölüm 8 — Sütun seçme ve ORDER BY
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
]
baglanti = sqlite3.connect("kutuphane.db")
imlec = baglanti.cursor()
imlec.execute("DROP TABLE IF EXISTS kitaplar")  # örneği her seferinde temiz başlat
imlec.execute("""CREATE TABLE kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    yazar TEXT NOT NULL,
    yil INTEGER,
    puan INTEGER DEFAULT 3)""")
imlec.executemany("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)", KITAPLAR)
baglanti.commit()

imlec.execute("SELECT ad, yil FROM kitaplar ORDER BY yil")
for ad, yil in imlec.fetchall():
    print(yil, ad)
baglanti.close()


# %% Bölüm 9 — LIMIT, fetchone ve toplama fonksiyonları
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
]
baglanti = sqlite3.connect("kutuphane.db")
imlec = baglanti.cursor()
imlec.execute("DROP TABLE IF EXISTS kitaplar")  # örneği her seferinde temiz başlat
imlec.execute("""CREATE TABLE kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    yazar TEXT NOT NULL,
    yil INTEGER,
    puan INTEGER DEFAULT 3)""")
imlec.executemany("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)", KITAPLAR)
baglanti.commit()

imlec.execute("SELECT ad, puan FROM kitaplar ORDER BY puan DESC, yil LIMIT 3")
print("İlk 3:", imlec.fetchall())

imlec.execute("SELECT COUNT(*), AVG(puan), MIN(yil), MAX(yil) FROM kitaplar")
sayi, ort, en_eski, en_yeni = imlec.fetchone()
print(f"{sayi} kitap · ortalama puan {ort:.2f} · {en_eski}–{en_yeni}")
baglanti.close()


# %% Bölüm 10 — sqlite3.Row ile sütun adıyla erişim
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
]
baglanti = sqlite3.connect("kutuphane.db")
imlec = baglanti.cursor()
imlec.execute("DROP TABLE IF EXISTS kitaplar")  # örneği her seferinde temiz başlat
imlec.execute("""CREATE TABLE kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    yazar TEXT NOT NULL,
    yil INTEGER,
    puan INTEGER DEFAULT 3)""")
imlec.executemany("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)", KITAPLAR)
baglanti.commit()

baglanti.row_factory = sqlite3.Row
for kitap in baglanti.execute("SELECT ad, yazar FROM kitaplar ORDER BY yil LIMIT 3"):
    print(kitap["ad"], "-", kitap["yazar"])
baglanti.close()


# %% Uygulama 1 — Kitaplık programı (menülü, kitaplik.db)
import sqlite3

baglanti = sqlite3.connect("kitaplik.db")
baglanti.execute("""CREATE TABLE IF NOT EXISTS kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL,
    yazar TEXT NOT NULL, yil INTEGER, puan INTEGER DEFAULT 3)""")


def kitap_ekle(ad, yazar, yil, puan):
    with baglanti:
        baglanti.execute("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)",
                         (ad, yazar, yil, puan))


def kitaplari_listele():
    satirlar = baglanti.execute("SELECT id, ad, yazar, yil, puan FROM kitaplar ORDER BY yil").fetchall()
    if not satirlar:
        print("Kitaplık boş.")
    for no, ad, yazar, yil, puan in satirlar:
        print(f"{no:>3}. {ad} — {yazar} ({yil}) · puan {puan}/5")


def istatistik():
    sayi, ort = baglanti.execute("SELECT COUNT(*), AVG(puan) FROM kitaplar").fetchone()
    if sayi:
        print(f"{sayi} kitap, ortalama puan {ort:.1f}")


while True:
    print("\n1) Ekle  2) Listele  3) İstatistik  0) Çıkış")
    secim = input("Seçim: ").strip()
    if secim == "1":
        ad = input("Kitap adı: ").strip()
        yazar = input("Yazar: ").strip()
        try:
            yil = int(input("Yıl: "))
            puan = int(input("Puan (1-5): "))
        except ValueError:
            print("Yıl ve puan sayı olmalı.")
            continue
        if not ad or not yazar or not 1 <= puan <= 5:
            print("Eksik ya da hatalı bilgi.")
            continue
        kitap_ekle(ad, yazar, yil, puan)
        print("Eklendi.")
    elif secim == "2":
        kitaplari_listele()
    elif secim == "3":
        istatistik()
    elif secim == "0":
        break
    else:
        print("Geçersiz seçim.")
baglanti.close()


# %% Uygulama 2 — Harcama defteri SQLite’ta
import sqlite3

HARCAMALAR = [("2026-10-20", "Market", 245.90),
              ("2026-10-21", "Ulaşım", 60.00),
              ("2026-10-23", "Kitap", 180.50)]
baglanti = sqlite3.connect("harcamalar.db")
with baglanti:
    baglanti.execute("""CREATE TABLE IF NOT EXISTS harcamalar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarih TEXT NOT NULL, aciklama TEXT NOT NULL, tutar REAL NOT NULL)""")
    baglanti.executemany("INSERT INTO harcamalar (tarih, aciklama, tutar) VALUES (?, ?, ?)",
                         HARCAMALAR)
adet, toplam = baglanti.execute("SELECT COUNT(*), SUM(tutar) FROM harcamalar").fetchone()
print(f"{adet} harcama, toplam {toplam:.2f} TL")
for tarih, aciklama, tutar in baglanti.execute(
        "SELECT tarih, aciklama, tutar FROM harcamalar ORDER BY tutar DESC"):
    print(f"{tarih}  {aciklama:<7}{tutar:>8.2f} TL")
baglanti.close()


# %% Alıştırma 1 — çözüm
import sqlite3

FILMLER = [("Eşkıya", "Yavuz Turgul", 1996),
           ("Babam ve Oğlum", "Çağan Irmak", 2005),
           ("Kış Uykusu", "Nuri Bilge Ceylan", 2014)]
baglanti = sqlite3.connect("filmler.db")
with baglanti:
    baglanti.execute("""CREATE TABLE IF NOT EXISTS filmler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL, yonetmen TEXT NOT NULL, yil INTEGER)""")
    baglanti.executemany("INSERT INTO filmler (ad, yonetmen, yil) VALUES (?, ?, ?)",
                         FILMLER)
for ad, yonetmen, yil in baglanti.execute("SELECT ad, yonetmen, yil FROM filmler ORDER BY yil"):
    print(f"{yil} · {ad} ({yonetmen})")
baglanti.close()


# %% Alıştırma 2 — çözüm
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
]
baglanti = sqlite3.connect(":memory:")
baglanti.execute("CREATE TABLE kitaplar (ad TEXT, yazar TEXT, yil INTEGER, puan INTEGER)")
baglanti.executemany("INSERT INTO kitaplar VALUES (?, ?, ?, ?)", KITAPLAR)
print("En yüksek puanlı 3 kitap:")
for ad, puan in baglanti.execute("SELECT ad, puan FROM kitaplar ORDER BY puan DESC, ad LIMIT 3"):
    print(f"  {ad} ({puan})")
ort_yil = baglanti.execute("SELECT AVG(yil) FROM kitaplar").fetchone()[0]
print(f"Ortalama yayın yılı: {ort_yil:.0f}")
baglanti.close()


# %% Alıştırma 3 — çözüm
import sqlite3


def kitap_ekle(baglanti, ad, yazar, yil, puan):
    if not 1 <= puan <= 5:
        raise ValueError("Puan 1 ile 5 arasında olmalı.")
    with baglanti:
        imlec = baglanti.execute("INSERT INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)",
                                 (ad, yazar, yil, puan))
    return imlec.lastrowid


baglanti = sqlite3.connect(":memory:")
baglanti.execute("""CREATE TABLE kitaplar (id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL, yazar TEXT NOT NULL, yil INTEGER, puan INTEGER)""")
for kitap in [("Tutunamayanlar", "Oğuz Atay", 1972, 5), ("Deneme", "Yazar", 2020, 9)]:
    try:
        print("Eklendi, id:", kitap_ekle(baglanti, *kitap))
    except ValueError as hata:
        print("Eklenmedi:", hata)
baglanti.close()
