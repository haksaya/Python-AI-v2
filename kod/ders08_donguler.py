# =============================================================================
# Python Kursu — Ders 8 (Hafta 4, Gün 2)
# Konu: for döngüsü, range, while döngüsü, break ve continue
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
#   - input() içeren hücreler klavyeden giriş bekler.
#   - Bir döngü durmazsa terminalde Ctrl+C ile durdurun (Jupyter'de Interrupt düğmesi).
# =============================================================================


# %% Ödev kontrolü — Ders 7 Ödev 1: VKİ
boy = float(input("Boy (m): ").replace(",", "."))
kilo = float(input("Kilo (kg): ").replace(",", "."))
vki = kilo / boy ** 2
if vki < 18.5:
    durum = "zayıf"
elif vki < 25:
    durum = "normal"
elif vki < 30:
    durum = "fazla kilolu"
else:
    durum = "obez"
print(f"VKİ: {vki:.2f} ({durum})")


# %% Bölüm 1 — İlk for döngüsü
notlar = [70, 45, 92]
for n in notlar:
    if n >= 50:
        print(n, "Geçti")
    else:
        print(n, "Kaldı")


# %% Bölüm 2 — for: her eleman için bir tur
sehirler = ["Ankara", "İzmir", "Bursa"]
for sehir in sehirler:
    print("Merhaba", sehir)
print("Döngü bitti.")


# %% Bölüm 3 — Metin ve sözlük üzerinde for
for harf in "Kedi":
    print(harf, end=" ")
print()
stok = {"kalem": 90, "defter": 45, "silgi": 60}
for urun in stok:
    print(urun)
for urun, adet in stok.items():
    print(f"{urun:<8}{adet:>4} adet")


# %% Bölüm 4 — range ile sayarak döngü
for i in range(3):
    print("Tekrar", i)
for kat in range(5, 0, -1):
    print(kat, end=" ")
print("Zemin!")


# %% Bölüm 5 — Biriktirme kalıbı: toplam ve sayaç
harcamalar = [120, 45, 300, 80, 15, 210]
toplam = 0
adet = 0
for tutar in harcamalar:
    toplam += tutar
    if tutar > 100:
        adet += 1
print("Toplam:", toplam)
print("100 TL üstü harcama:", adet)


# %% Bölüm 6 — Filtreleme ve en büyüğü bulma
notlar = [78, 45, 92, 30, 66, 85]
gecenler = []
en_yuksek = notlar[0]
for n in notlar:
    if n >= 50:
        gecenler.append(n)
    if n > en_yuksek:
        en_yuksek = n
print("Geçenler:", gecenler)
print("En yüksek:", en_yuksek)
print("Kısa yol:", [n for n in notlar if n >= 50])


# %% Bölüm 7 — enumerate ve zip
ogrenciler = ["Ayşe", "Mehmet", "Zeynep"]
notlar = [88, 64, 95]
for sira, ad in enumerate(ogrenciler, start=1):
    print(f"{sira}. {ad}")
for ad, puan in zip(ogrenciler, notlar):
    print(f"{ad}: {puan}")


# %% Bölüm 8 — while: koşul doğru olduğu sürece
bakiye = 1000
ay = 0
while bakiye < 1500:
    bakiye = bakiye * 1.04
    ay += 1
print(f"{ay} ay sonra bakiye: {bakiye:.2f} TL")


# %% Bölüm 9 — while ile doğru girene kadar sormak
yas = input("Yaşınız: ")
while not yas.isdigit():
    print("Lütfen rakamla yazın.")
    yas = input("Yaşınız: ")
yas = int(yas)
print(f"Teşekkürler, {yas} yaşındasınız.")


# %% Bölüm 10 — break ve continue
sepet = ["süt", "ekmek", "SKT geçmiş peynir", "yumurta", "DUR", "çay"]
for urun in sepet:
    if urun == "DUR":
        print("Kasaya gidiliyor.")
        break
    if "SKT geçmiş" in urun:
        print("Atlandı:", urun)
        continue
    print("Sepete eklendi:", urun)


# %% Bölüm 11 — while True ve break
while True:
    komut = input("Komut (q: çıkış): ").strip().lower()
    if komut == "q":
        print("Görüşmek üzere!")
        break
    if not komut:
        continue
    print(f"'{komut}' komutu çalıştırıldı.")


# %% Bölüm 12 — İç içe döngüler: çarpım tablosu
for satir in range(1, 4):
    for sutun in range(1, 6):
        print(f"{satir * sutun:>4}", end="")
    print()


# %% Uygulama 1 — Sayı tahmin oyunu
import random

gizli = random.randint(1, 100)
hak = 7

while hak > 0:
    tahmin = int(input("Tahmininiz: "))
    hak -= 1
    if tahmin == gizli:
        print(f"Bildiniz! {7 - hak}. denemede.")
        break
    elif tahmin < gizli:
        print(f"Daha büyük. (kalan hak: {hak})")
    else:
        print(f"Daha küçük. (kalan hak: {hak})")

if tahmin != gizli:
    print(f"Hakkınız bitti. Sayı {gizli} idi.")


# %% Uygulama 2 — Aylık harcama analizi
harcamalar = [
    ("market", 450.75), ("ulaşım", 120.00), ("market", 89.90),
    ("eğlence", 300.00), ("fatura", 850.00), ("ulaşım", 45.50),
    ("market", 230.40), ("eğlence", 150.00),
]
kategori_toplam = {}
for kategori, tutar in harcamalar:
    kategori_toplam[kategori] = kategori_toplam.get(kategori, 0) + tutar
genel = sum(kategori_toplam.values())
for kategori, toplam in kategori_toplam.items():
    oran = toplam / genel * 100
    print(f"{kategori:<9}{toplam:>9.2f} TL  %{oran:4.1f}")
print(f"{'TOPLAM':<9}{genel:>9.2f} TL")


# %% Alıştırma 1 — çözüm
toplam = 0
for i in range(1, 11):
    kare = i ** 2
    print(i, "→", kare)
    toplam += kare
print("Toplam:", toplam)


# %% Alıştırma 2 — çözüm
metin = "Python öğrenmek sabır ve düzenli pratik gerektirir"
uzunlar, en_uzun = [], ""
for k in metin.split():
    if len(k) > 5:
        uzunlar.append(k)
    if len(k) > len(en_uzun):
        en_uzun = k
print(uzunlar)
print(len(uzunlar), "kelime; en uzun:", en_uzun)


# %% Alıştırma 3 — çözüm (düzeltilmiş)
notlar = [70, 80, 90]
toplam = 0
for n in notlar:
    toplam += n
print(toplam / len(notlar))
for n in notlar:
    print(n)


# %% Alıştırma 4 — çözüm
dogru_pin = "2580"
hak = 3
while hak > 0:
    pin = input("PIN: ")
    if pin == dogru_pin:
        print("Hoş geldiniz.")
        break
    hak -= 1
    if hak > 0:
        print(f"Hatalı PIN. Kalan hak: {hak}")
    else:
        print("Kartınız bloke edildi.")


# %% Ek — Gelecek dersin önizlemesi: fonksiyonlar
def harf_notu(puan):
    if puan >= 85:
        return "BA ve üstü"
    return "BA altı"

print(harf_notu(92))
