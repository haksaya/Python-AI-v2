# =============================================================================
# Python Kursu — Ders 4 (Hafta 2, Gün 2)
# Konu: Gömülü fonksiyonlar, en çok kullanılanlar, fonksiyon ve metot farkı
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - DİKKAT: input() içeren hücreler (Uygulama 2) klavyeden giriş bekler.
#   - Bölüm 8'deki help() çıktısı uzundur; terminalde açılırsa "q" ile çıkın.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
# =============================================================================


# %% Bölüm 1 — Fonksiyon çağırmak: ad + parantez + argüman -> dönüş değeri
uzunluk = len("Python")          # len'e "Python" verdik, 6 geri döndü
print(uzunluk)                   # 6
print(len("Python") * 2)         # 12 -> dönüş değeri doğrudan işlemde kullanılabilir
print(len("Merhaba Dünya"))      # 13 -> boşluk da sayılır


# %% Bölüm 2 — Şimdiye kadar kullandığımız gömülü fonksiyonlar
print("print ekrana yazar")
print(type(3.5))                 # <class 'float'>
print(int("42") + 1)             # 43
print(float("2.5") * 2)          # 5.0
print(str(7) + " gün")           # 7 gün
print(bool(""))                  # False
print(len("İstanbul"))           # 8


# %% Bölüm 3 — Sayılarla çalışan fonksiyonlar: abs, round, pow, divmod
print(abs(-7))                   # 7     -> mutlak değer
print(abs(3.5))                  # 3.5
print(round(3.14159, 2))         # 3.14  -> 2 basamağa yuvarla
print(round(3.7))                # 4     -> basamak verilmezse tam sayıya
print(round(1234.5678, -2))      # 1200.0 -> negatif basamak: yüzlere yuvarla
print(pow(2, 10))                # 1024  -> 2 ** 10 ile aynı
print(divmod(17, 5))             # (3, 2) -> (17 // 5, 17 % 5) birlikte

# Yuvarlama sürprizi (Ders 3'teki kuralın aynısı): tam ortada ÇİFTE yuvarlar
print(round(2.5))                # 2  (3 değil!)
print(round(3.5))                # 4
print(round(0.5))                # 0


# %% Bölüm 4 — Bir grup değerle çalışan fonksiyonlar: min, max, sum, len
# Köşeli parantezle yazılan [ ... ] bir LİSTEDİR (ayrıntısı Ders 5'te).
notlar = [78, 92, 65, 88, 71, 95, 54]

print(len(notlar))               # 7   -> kaç not var
print(sum(notlar))               # 543 -> toplam
print(min(notlar))               # 54  -> en düşük
print(max(notlar))               # 95  -> en yüksek

ortalama = sum(notlar) / len(notlar)
print(ortalama)                  # 77.57142857142857
print(round(ortalama, 1))        # 77.6
print(f"{ortalama:.1f}")         # 77.6 -> ekranda göstermek için f-string de olur

# min ve max liste olmadan, virgülle ayrılmış değerlerle de çalışır
print(max(3, 9, 4))              # 9
print(min(85.5, 79.9, 92.0))     # 79.9


# %% Bölüm 5 — sorted: sıralanmış YENİ bir liste döndürür
notlar = [78, 92, 65, 88, 71, 95, 54]

print(sorted(notlar))                  # [54, 65, 71, 78, 88, 92, 95]
print(sorted(notlar, reverse=True))    # [95, 92, 88, 78, 71, 65, 54]
print(notlar)                          # [78, 92, 65, 88, 71, 95, 54] -> orijinal değişmedi
print(sorted("python"))                # ['h', 'n', 'o', 'p', 't', 'y'] -> metnin harfleri


# %% Bölüm 6 — Türkçe sıralama tuzağı
isimler = ["Zeynep", "ali", "Çağrı", "Ayşe"]
print(sorted(isimler))     # ['Ayşe', 'Zeynep', 'ali', 'Çağrı'] -> beklenen bu değil!
# Neden? Python harfleri bilgisayardaki kod numaralarına göre sıralar:
print(ord("A"), ord("Z"), ord("a"), ord("Ç"))   # 65 90 97 199
# Büyük harfler küçüklerden, Türkçe harfler tüm İngilizce harflerden sonra gelir.
# Tam Türkçe sıralama için ek araçlar gerekir; şimdilik bu davranışı bilmek yeterli.


# %% Bölüm 7 — Fonksiyon mu, metot mu?
metin = "merhaba"

print(len(metin))          # 7       -> FONKSİYON: değer parantez içinde
print(metin.upper())       # MERHABA -> METOT: değerden sonra nokta

# Fonksiyon farklı tiplerle çalışabilir:
print(len("abc"), len([1, 2, 3]))      # 3 3
# Metot ise yalnızca ait olduğu tipte vardır:
#   [1, 2, 3].upper()  -> AttributeError: 'list' object has no attribute 'upper'


# %% Bölüm 8 — Her fonksiyon bir değer döndürmez: print -> None
sonuc = print("Merhaba")   # ekrana Merhaba yazar...
print(sonuc)               # None   -> ...ama geriye bir şey döndürmez
print(type(sonuc))         # <class 'NoneType'>


# %% Bölüm 9 — Yardım almak: help() ve dir()
help(round)                # round'un açıklamasını gösterir (terminalde "q" ile çıkın)
print(dir("metin")[-10:])  # bir metnin metotlarından son 10 tanesi


# %% Bölüm 10 — Gömülü fonksiyonların adını değişken yapmayın! (düzeltilmiş hali)
# Hatalı:
#   len = 5
#   print(len("abc"))   -> TypeError: 'int' object is not callable
uzunluk = 5                # başka bir ad seçin
print(len("abc"))          # 3


# %% Uygulama 1 — Sınıf not analizi
notlar = [78, 92, 65, 88, 71, 95, 54]

ogrenci_sayisi = len(notlar)
ortalama = sum(notlar) / ogrenci_sayisi
en_yuksek = max(notlar)
en_dusuk = min(notlar)
aciklik = en_yuksek - en_dusuk
sirali = sorted(notlar)
ortanca = sirali[ogrenci_sayisi // 2]      # tek sayıda not olduğu için ortadaki

print(f"{'Öğrenci sayısı':<16}: {ogrenci_sayisi}")
print(f"{'Ortalama':<16}: {ortalama:.1f}")
print(f"{'En yüksek':<16}: {en_yuksek}")
print(f"{'En düşük':<16}: {en_dusuk}")
print(f"{'Açıklık':<16}: {aciklik}")
print(f"{'Ortanca':<16}: {ortanca}")
print(f"{'Sıralı notlar':<16}: {sirali}")


# %% Uygulama 2 — Üç mağazanın fiyat karşılaştırması  [GİRİŞ BEKLER]
fiyat1 = float(input("1. mağaza fiyatı: ").replace(",", "."))   # örnek: 1249,90
fiyat2 = float(input("2. mağaza fiyatı: ").replace(",", "."))   # örnek: 1199
fiyat3 = float(input("3. mağaza fiyatı: ").replace(",", "."))   # örnek: 1315,50

en_ucuz = min(fiyat1, fiyat2, fiyat3)
en_pahali = max(fiyat1, fiyat2, fiyat3)
ortalama = (fiyat1 + fiyat2 + fiyat3) / 3
fark = en_pahali - en_ucuz

print(f"{'En ucuz':<15}: {en_ucuz:.2f} TL")
print(f"{'En pahalı':<15}: {en_pahali:.2f} TL")
print(f"{'Ortalama':<15}: {ortalama:.2f} TL")
print(f"{'Tasarruf':<15}: {fark:.2f} TL")
print(f"{'Tasarruf oranı':<15}: %{fark / en_pahali * 100:.1f}")


# =============================================================================
# SINIF İÇİ ALIŞTIRMALARIN ÇÖZÜMLERİ
# =============================================================================

# %% Alıştırma 1 (kolay) — Tek satırlık sorular
print(abs(-15))               # 15
print(round(9.876, 1))        # 9.9
print(len("Programlama"))     # 11
print(max(12, 7, 21, 3))      # 21
print(divmod(100, 7))         # (14, 2)


# %% Alıştırma 2 (kolay-orta) — Fiyat listesi
fiyatlar = [349.90, 129.50, 899.00, 74.25, 450.00]
print("Ürün sayısı:", len(fiyatlar))
print("En ucuz:", min(fiyatlar))
print("En pahalı:", max(fiyatlar))
print(f"Toplam: {sum(fiyatlar):.2f} TL")
print(f"Ortalama: {sum(fiyatlar) / len(fiyatlar):.2f} TL")
print("Ucuzdan pahalıya:", sorted(fiyatlar))


# %% Alıştırma 3 (orta) — Hata avı (düzeltilmiş hali)
# Hatalı hali:
#   notlar = [80, 95, 70]
#   toplam = sum(notlar)
#   print("Ortalama: " + toplam / len(notlar))
#   print("En yüksek:", Max(notlar))
#   print("Sıralı:", notlar.sorted())
notlar = [80, 95, 70]
toplam = sum(notlar)
print("Ortalama: " + str(toplam / len(notlar)))
print("En yüksek:", max(notlar))
print("Sıralı:", sorted(notlar))


# %% Alıştırma 4 (zor) — En düşük not silinerek ortalama
notlar = [72, 85, 90, 64, 88]

normal_ortalama = sum(notlar) / len(notlar)
yeni_ortalama = (sum(notlar) - min(notlar)) / (len(notlar) - 1)
sirali = sorted(notlar)

print(f"Normal ortalama        : {normal_ortalama:.2f}")
print(f"En düşük silinince     : {yeni_ortalama:.2f}")
print(f"Kazanç                 : {yeni_ortalama - normal_ortalama:.2f} puan")
print(f"Açıklık (max - min)    : {max(notlar) - min(notlar)}")
print(f"Ortanca                : {sirali[len(notlar) // 2]}")


# %% Ek — Gelecek dersin önizlemesi: listeler
notlar = [78, 92, 65]
notlar.append(100)         # listeye eleman ekleyen bir METOT
print(notlar)              # [78, 92, 65, 100]
