# =============================================================================
# Python Kursu — Ders 5 (Hafta 3, Gün 1)
# Konu: Listeler ve demetler (tuple), liste metotları
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
#   - Ödev kontrolü hücresi klavyeden giriş bekler (ör. 148).
# =============================================================================


# %% Ödev kontrolü — Ders 4 Ödev 2: film süresi
dakika = int(input("Film kaç dakika? "))
saat, kalan = divmod(dakika, 60)
print(f"{saat} saat {kalan} dakika")


# %% Bölüm 1 — Liste oluşturmak
alisveris = ["ekmek", "süt", "yumurta"]
notlar = [78, 92, 65]
karisik = ["Ali", 34, 1.75, True]
bos = []
print(alisveris)
print(len(alisveris), len(bos))


# %% Bölüm 2 — list(), split(), range(), + ve *
harfler = list("Python")
print(harfler)
kelimeler = "elma armut kiraz".split()
print(kelimeler)
sayilar = list(range(1, 6))
print(sayilar)
print([0] * 4)
print([1, 2] + [3, 4])


# %% Bölüm 3 — İndeks ve dilim
alisveris = ["ekmek", "süt", "yumurta", "peynir", "çay"]
print(alisveris[0])
print(alisveris[-1])
print(alisveris[1:3])
print(alisveris[:2])
print(alisveris[::-1])


# %% Bölüm 4 — Liste değiştirilebilir (mutable)
alisveris = ["ekmek", "süt", "yumurta"]
alisveris[1] = "ayran"
print(alisveris)
alisveris[0] = alisveris[0].upper()
print(alisveris)


# %% Bölüm 5 — Eleman ekleme: append, insert, extend
alisveris = ["ekmek", "süt"]
alisveris.append("yumurta")
print(alisveris)
alisveris.insert(0, "su")
print(alisveris)
alisveris.extend(["çay", "şeker"])
print(alisveris)
print(len(alisveris))


# %% Bölüm 6 — append ile extend farkı
a = [1, 2]
a.append([3, 4])
print(a, len(a))
b = [1, 2]
b.extend([3, 4])
print(b, len(b))


# %% Bölüm 7 — Silme: remove, pop, del, clear
alisveris = ["su", "ekmek", "süt", "çay", "şeker"]
alisveris.remove("süt")
print(alisveris)
son = alisveris.pop()
print(son, alisveris)
ilk = alisveris.pop(0)
print(ilk, alisveris)
del alisveris[0]
print(alisveris)
alisveris.clear()
print(alisveris)


# %% Bölüm 8 — Arama: in, not in, index, count
sepet = ["elma", "süt", "elma", "ekmek", "elma"]
print("süt" in sepet)
print("çay" in sepet)
print("çay" not in sepet)
print(sepet.index("ekmek"))
print(sepet.count("elma"))


# %% Bölüm 9 — sort ile sorted farkı
notlar = [72, 95, 64, 88]
sirali = sorted(notlar)
print(sirali, notlar)
notlar.sort()
print(notlar)
notlar.sort(reverse=True)
print(notlar)


# %% Bölüm 10 — Tuzak: liste = liste.sort()
notlar = [72, 95, 64]
notlar = notlar.sort()
print(notlar)


# %% Bölüm 11 — Kopyalama tuzağı ve copy()
a = ["ekmek", "süt"]
b = a
b.append("çay")
print(a)
c = a.copy()
c.append("şeker")
print(a)
print(c)


# %% Bölüm 12 — Demet oluşturmak
konum = (41.0082, 28.9784)
dogum = (15, "Mart", 1990)
print(konum[0])
print(dogum[-1])
print(len(dogum))
print(type(konum))


# %% Bölüm 13 — Demet açma ve değer takası
konum = (41.0082, 28.9784)
enlem, boylam = konum
print("Enlem:", enlem, "Boylam:", boylam)
saat, dakika = divmod(130, 60)
print(saat, dakika)
a, b = 1, 2
a, b = b, a
print(a, b)


# %% Bölüm 14 — Tek elemanlı demet
x = (5)
y = (5,)
print(type(x), type(y))


# %% Uygulama 1 — Alışveriş listesi yönetimi
alisveris = ["ekmek", "süt", "yumurta"]
alisveris.append("domates")
alisveris.insert(0, "su")
alisveris.extend(["peynir", "zeytin"])
alisveris.remove("süt")
alinan = alisveris.pop(0)
alisveris[1] = "köy yumurtası"
alisveris.sort()
print("Alınan:", alinan)
print("Kalan ürün sayısı:", len(alisveris))
print("Liste:", ", ".join(alisveris))
print("Peynir var mı?", "peynir" in alisveris)


# %% Uygulama 2 — Kargo teslimat rotası (liste + demet)
depo = (0, 0)
duraklar = [("Fırın", 2, 3), ("Eczane", 5, 1), ("Market", 1, 6)]
duraklar.append(("Kırtasiye", 4, 4))
duraklar.insert(0, ("Hastane", 1, 1))
ad, x, y = duraklar[0]
mesafe = abs(x - depo[0]) + abs(y - depo[1])
print(f"İlk durak: {ad} ({x}, {y}) - {mesafe} blok")
son_ad, son_x, son_y = duraklar[-1]
print(f"Son durak: {son_ad} ({son_x}, {son_y})")
print("Durak sayısı:", len(duraklar))
duraklar.reverse()
print("Dönüş rotasında ilk:", duraklar[0][0])


# %% Alıştırma 1 — çözüm
yapilacaklar = []
yapilacaklar.append("fatura öde")
yapilacaklar.append("spor")
yapilacaklar.append("kitap oku")
yapilacaklar.remove("spor")
yapilacaklar.insert(0, "su iç")
print(yapilacaklar)
print(len(yapilacaklar))


# %% Alıştırma 2 — çözüm
notlar = [55, 78, 92, 40, 66]
notlar.remove(40)
notlar.append(85)
notlar.sort(reverse=True)
print(notlar)
print(notlar[:3])


# %% Alıştırma 3 — çözüm (düzeltilmiş)
renkler = ["kırmızı", "mavi"]
renkler.append("yeşil")
sehirler = ["Ankara", "İzmir"]
sehirler.sort()
print(sehirler[0])
print(sehirler[1])


# %% Alıştırma 4 — çözüm
koltuklar = ["A1", "A2", "A3", "B1", "B2"]
satilanlar = []

koltuklar.remove("A2")
satilanlar.append("A2")
koltuklar.remove("B1")
satilanlar.append("B1")

print("Boş koltuklar:", koltuklar)
print("Boş koltuk sayısı:", len(koltuklar))
print("Satılan koltuk sayısı:", len(satilanlar))
print("A3 boş mu?", "A3" in koltuklar)
print("Satılanlar:", tuple(satilanlar))


# %% Ek — Gelecek dersin önizlemesi: sözlükler
rehber = {"Ayşe": "0532 111 22 33"}
rehber["Mehmet"] = "0505 444 55 66"
print(rehber["Ayşe"])
