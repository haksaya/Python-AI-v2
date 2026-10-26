# =============================================================================
# Python Kursu — Ders 15 (Hafta 8, Gün 1)
# Konu: WHERE, karşılaştırma işleçleri, BETWEEN, IN, IS NULL, LIKE, AND/OR/NOT, UPDATE, DELETE, UNIQUE ve INSERT OR IGNORE, GROUP BY — kitaplık yönetimi mini projesi
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - sqlite3 modülü Python ile gelir; kurulum gerekmez.
#   - Örnekler çalışma klasöründe kutuphane.db ve kitaplik_yonetim.db dosyalarını oluşturur.
#   - SELECT örneklerinin her biri tabloyu baştan kurar (DROP TABLE IF EXISTS); kendi verilerinizle denerken bu satırı kaldırın.
# =============================================================================


# %% Bölüm 1 — WHERE ile filtreleme
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

imlec.execute("SELECT ad, yil FROM kitaplar"
              " WHERE yil < 1960 ORDER BY yil")
for ad, yil in imlec.fetchall():
    print(yil, ad)
baglanti.close()


# %% Bölüm 2 — Kullanıcının verdiği değerle WHERE
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

yazar = input("Yazar: ")
imlec.execute("SELECT ad, yil FROM kitaplar WHERE yazar = ? ORDER BY yil", (yazar,))
for ad, yil in imlec.fetchall():
    print(f"  {ad} ({yil})")
baglanti.close()


# %% Bölüm 3 — BETWEEN ve IN
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

imlec.execute("SELECT ad, yil FROM kitaplar WHERE yil BETWEEN 1950 AND 1979")
print("1950–1979:", [ad for ad, yil in imlec.fetchall()])
imlec.execute("SELECT COUNT(*) FROM kitaplar WHERE puan IN (4, 5)")
print("Puanı 4 ya da 5 olan:", imlec.fetchone()[0])
baglanti.close()


# %% Bölüm 4 — NULL ve IS NULL
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

imlec.execute("SELECT ad FROM kitaplar WHERE yil = NULL")
print("= NULL ile:", imlec.fetchall())
imlec.execute("SELECT ad FROM kitaplar WHERE yil IS NULL")
print("IS NULL ile:", imlec.fetchall())
imlec.execute("SELECT COUNT(*), COUNT(yil) FROM kitaplar")
print("Satır sayısı, yılı dolu olan:", imlec.fetchone())
baglanti.close()


# %% Bölüm 5 — LIKE ile arama
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

for kalip in ["%Ali%", "K%", "%a_a%"]:
    imlec.execute("SELECT ad FROM kitaplar WHERE ad LIKE ? OR yazar LIKE ?", (kalip, kalip))
    print(f"{kalip:<6} →", [ad for (ad,) in imlec.fetchall()])
baglanti.close()


# %% Bölüm 6 — LIKE ve Türkçe harfler
import sqlite3

baglanti = sqlite3.connect(":memory:")
baglanti.execute("CREATE TABLE kitaplar (ad TEXT)")
baglanti.executemany("INSERT INTO kitaplar VALUES (?)",
                     [("İnce Memed",), ("Kürk Mantolu Madonna",), ("Şeker Portakalı",)])
for kalip in ["%ince%", "%İnce%", "kürk%", "%şeker%"]:
    sonuc = baglanti.execute("SELECT ad FROM kitaplar WHERE ad LIKE ?", (kalip,)).fetchall()
    print(f"{kalip:<9}", sonuc)


# %% Bölüm 7 — Türkçe duyarlı arama: create_function
import sqlite3


def tr_kucuk(metin):
    """Türkçe kurallara göre küçük harfe çevirir."""
    return metin.replace("İ", "i").replace("I", "ı").lower()


baglanti = sqlite3.connect(":memory:")
baglanti.create_function("tr_kucuk", 1, tr_kucuk)
baglanti.execute("CREATE TABLE kitaplar (ad TEXT)")
baglanti.executemany("INSERT INTO kitaplar VALUES (?)",
                     [("İnce Memed",), ("Kürk Mantolu Madonna",), ("Şeker Portakalı",)])
for aranan in ["ince", "ŞEKER", "IŞIK"]:
    kalip = f"%{tr_kucuk(aranan)}%"
    sonuc = baglanti.execute("SELECT ad FROM kitaplar WHERE tr_kucuk(ad) LIKE ?", (kalip,)).fetchall()
    print(f"{aranan:<6}", sonuc)


# %% Bölüm 8 — AND, OR, NOT ve parantez
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

imlec.execute("""SELECT ad, yazar, puan FROM kitaplar
                 WHERE (yazar = ? OR yazar = ?) AND NOT puan < 4""",
              ("Sabahattin Ali", "Oğuz Atay"))
for satir in imlec.fetchall():
    print(satir)
baglanti.close()


# %% Bölüm 9 — UPDATE
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

imlec.execute("UPDATE kitaplar SET puan = ? WHERE ad = ?",
              (5, "İnce Memed"))
print("Değişen satır:", imlec.rowcount)
baglanti.commit()
imlec.execute("SELECT ad, puan FROM kitaplar WHERE ad = ?",
              ("İnce Memed",))
print(imlec.fetchone())
baglanti.close()


# %% Bölüm 10 — WHERE’siz UPDATE ve rollback
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

imlec.execute("UPDATE kitaplar SET puan = 1")   # WHERE unutuldu!
print("Değişen satır:", imlec.rowcount)
baglanti.rollback()                             # commit edilmedi: geri al
imlec.execute("SELECT COUNT(*) FROM kitaplar WHERE puan = 1")
print("Geri alındıktan sonra puanı 1 olan:", imlec.fetchone()[0])
baglanti.close()


# %% Bölüm 11 — DELETE
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

imlec.execute("SELECT id, ad FROM kitaplar WHERE yil IS NULL")
print("Silinecek:", imlec.fetchall())
imlec.execute("DELETE FROM kitaplar WHERE yil IS NULL")
print("Silinen satır:", imlec.rowcount)
baglanti.commit()
imlec.execute("SELECT COUNT(*) FROM kitaplar")
print("Kalan kitap:", imlec.fetchone()[0])
baglanti.close()


# %% Bölüm 12 — UNIQUE ve INSERT OR IGNORE
import sqlite3

baglanti = sqlite3.connect(":memory:")
baglanti.execute("""CREATE TABLE kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL, yazar TEXT NOT NULL,
    UNIQUE (ad, yazar))""")
for _ in range(3):  # aynı kitabı üç kez eklemeyi dene
    imlec = baglanti.execute("INSERT OR IGNORE INTO kitaplar (ad, yazar)"
                             " VALUES (?, ?)",
                             ("Tutunamayanlar", "Oğuz Atay"))
    print("Eklenen:", imlec.rowcount)
toplam = baglanti.execute("SELECT COUNT(*) FROM kitaplar").fetchone()[0]
print("Toplam:", toplam)


# %% Bölüm 13 — GROUP BY ile gruplayarak sayma
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

imlec.execute("""SELECT yazar, COUNT(*), AVG(puan) FROM kitaplar
                 GROUP BY yazar ORDER BY COUNT(*) DESC, yazar LIMIT 3""")
for yazar, sayi, ort in imlec.fetchall():
    print(f"{yazar:<22}{sayi} kitap · ort. puan {ort:.1f}")
baglanti.close()


# %% Mini proje — Kitaplık yönetimi (arama, güncelleme, silme)
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
]


def tr_kucuk(metin):
    return metin.replace("İ", "i").replace("I", "ı").lower()


def baglan(dosya="kitaplik_yonetim.db"):
    baglanti = sqlite3.connect(dosya)
    baglanti.create_function("tr_kucuk", 1, tr_kucuk)
    with baglanti:
        baglanti.execute("""CREATE TABLE IF NOT EXISTS kitaplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL, yazar TEXT NOT NULL,
            yil INTEGER, puan INTEGER DEFAULT 3, UNIQUE (ad, yazar))""")
        baglanti.executemany("INSERT OR IGNORE INTO kitaplar (ad, yazar, yil, puan) VALUES (?, ?, ?, ?)",
                             KITAPLAR)
    return baglanti


def yazdir(satirlar):
    if not satirlar:
        print("Kayıt bulunamadı.")
    for no, ad, yazar, yil, puan in satirlar:
        print(f"{no:>3}. {ad} — {yazar} ({yil or '?'}) · {puan}/5")


def ara(baglanti, metin):
    kalip = f"%{tr_kucuk(metin)}%"
    return baglanti.execute("""SELECT id, ad, yazar, yil, puan FROM kitaplar
        WHERE tr_kucuk(ad) LIKE ? OR tr_kucuk(yazar) LIKE ? ORDER BY ad""", (kalip, kalip)).fetchall()


def puan_guncelle(baglanti, kitap_id, puan):
    if not 1 <= puan <= 5:
        raise ValueError("Puan 1 ile 5 arasında olmalı.")
    with baglanti:
        return baglanti.execute("UPDATE kitaplar SET puan = ? WHERE id = ?", (puan, kitap_id)).rowcount


def kitap_sil(baglanti, kitap_id):
    with baglanti:
        return baglanti.execute("DELETE FROM kitaplar WHERE id = ?", (kitap_id,)).rowcount


baglanti = baglan()
while True:
    print("\n1) Ara 2) Puan 3) Sil 4) İstatistik 0) Çıkış")
    secim = input("Seçim: ").strip()
    try:
        if secim == "1":
            yazdir(ara(baglanti, input("Aranan (ad/yazar): ").strip()))
        elif secim == "2":
            kitap_id, puan = int(input("Kitap no: ")), int(input("Yeni puan: "))
            print("Güncellendi." if puan_guncelle(baglanti, kitap_id, puan) else "Bu numarada kitap yok.")
        elif secim == "3":
            kitap_id = int(input("Silinecek kitap no: "))
            if input("Emin misiniz? (e/h): ").strip().lower() == "e":
                print("Silindi." if kitap_sil(baglanti, kitap_id) else "Bu numarada kitap yok.")
        elif secim == "4":
            for yazar, sayi in baglanti.execute("SELECT yazar, COUNT(*) FROM kitaplar"
                                                " GROUP BY yazar HAVING COUNT(*) > 1"):
                print(f"{yazar}: {sayi} kitap")
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")
    except ValueError as hata:
        print("Hatalı giriş:", hata)
baglanti.close()


# %% Alıştırma 1 — çözüm
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

yazar = "Sabahattin Ali"
for ad, yil in imlec.execute("SELECT ad, yil FROM kitaplar WHERE yazar = ? ORDER BY yil", (yazar,)):
    print(yil, ad)
sayi = imlec.execute("SELECT COUNT(*) FROM kitaplar WHERE yazar = ?", (yazar,)).fetchone()[0]
print(f"{yazar}: {sayi} kitap")
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
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

kosul = "WHERE yil BETWEEN 1950 AND 1979"
print("Önce:", imlec.execute(f"SELECT ad, puan FROM kitaplar {kosul}").fetchall())
imlec.execute(f"UPDATE kitaplar SET puan = MIN(puan + 1, 5) {kosul}")
print("Değişen:", imlec.rowcount)
baglanti.commit()
print("Sonra:", imlec.execute(f"SELECT ad, puan FROM kitaplar {kosul}").fetchall())
baglanti.close()


# %% Alıştırma 3 — çözüm
import sqlite3

KITAPLAR = [
    ("Tutunamayanlar", "Oğuz Atay", 1972, 5),
    ("İnce Memed", "Yaşar Kemal", 1955, 4),
    ("Saatleri Ayarlama Enstitüsü", "Ahmet Hamdi Tanpınar", 1961, 5),
    ("Kürk Mantolu Madonna", "Sabahattin Ali", 1943, 4),
    ("Puslu Kıtalar Atlası", "İhsan Oktay Anar", 1995, 4),
    ("Kuyucaklı Yusuf", "Sabahattin Ali", 1937, 3),
    ("Benim Adım Kırmızı", "Orhan Pamuk", 1998, 3),
    ("Semaver", "Sait Faik Abasıyanık", None, 3),
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

def sil_onayli(baglanti, kitap_id):
    satir = baglanti.execute("SELECT ad FROM kitaplar WHERE id = ?",
                             (kitap_id,)).fetchone()
    if satir is None:
        print("Kitap bulunamadı.")
        return False
    cevap = input(f"“{satir[0]}” silinsin mi? (e/h): ")
    if cevap.strip().lower() != "e":
        print("Vazgeçildi.")
        return False
    with baglanti:
        baglanti.execute("DELETE FROM kitaplar WHERE id = ?",
                         (kitap_id,))
    print("Silindi.")
    return True


print(sil_onayli(baglanti, 99))
print(sil_onayli(baglanti, 6))
print("Kalan:", baglanti.execute("SELECT COUNT(*) FROM kitaplar").fetchone()[0])
baglanti.close()
