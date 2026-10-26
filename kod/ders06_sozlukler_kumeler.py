# =============================================================================
# Python Kursu — Ders 6 (Hafta 3, Gün 2)
# Konu: Sözlükler (dict), dict metotları, kümeler (set)
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
# =============================================================================


# %% Ödev kontrolü — Ders 5 Ödev 2: şehir bilgileri
sehirler = [("İstanbul", 15.7, 34), ("Ankara", 5.8, 6),
            ("İzmir", 4.5, 35)]
ad, nufus, plaka = sehirler[0]
print(f"{ad}: {nufus} milyon, plaka {plaka}")
en_kalabalik = max(sehirler[0][1], sehirler[1][1],
                   sehirler[2][1])
print("En kalabalık nüfus:", en_kalabalik)


# %% Bölüm 1 — Sözlük oluşturmak
rehber = {
    "Ayşe": "05321112233",
    "Mehmet": "05054445566",
    "Zeynep": "05427778899",
}
print(rehber)
print(len(rehber))
print(rehber["Mehmet"])


# %% Bölüm 2 — Farklı tipte anahtar ve değerler
plakalar = {34: "İstanbul", 6: "Ankara", 35: "İzmir"}
print(plakalar[6])
urun = {"ad": "Kalem", "fiyat": 7.5, "stokta": True}
print(urun["fiyat"] * 3)
bos = {}
print(type(bos), len(bos))


# %% Bölüm 2b — Aynı veri liste olarak
rehber_liste = [("Ayşe", "0532"), ("Mehmet", "0505"),
                ("Zeynep", "0542")]
print(rehber_liste[1][1])


# %% Bölüm 2c — Aynı veri sözlük olarak
rehber = {"Ayşe": "0532", "Mehmet": "0505",
          "Zeynep": "0542"}
print(rehber["Mehmet"])


# %% Bölüm 3 — get() ve in ile güvenli erişim
rehber = {"Ayşe": "0532 111 22 33",
          "Mehmet": "0505 444 55 66"}
print(rehber.get("Ayşe"))
print(rehber.get("Can"))
print(rehber.get("Can", "kayıtlı değil"))
print("Can" in rehber)


# %% Bölüm 4 — Ekleme, güncelleme, update()
stok = {"kalem": 120, "defter": 45}
stok["silgi"] = 60
print(stok)
stok["kalem"] = 100
print(stok)
stok["defter"] += 15
print(stok["defter"])
stok.update({"cetvel": 30, "silgi": 55})
print(stok)


# %% Bölüm 5 — Silme: del, pop, clear
rehber = {"Ayşe": "0532", "Mehmet": "0505", "Zeynep": "0542", "Can": "0555"}
del rehber["Can"]
print(rehber)
silinen = rehber.pop("Mehmet")
print("Silinen numara:", silinen)
print(rehber.pop("Ali", "zaten yok"))
print(rehber)


# %% Bölüm 6 — keys(), values(), items()
stok = {"kalem": 120, "defter": 60, "silgi": 55}
print(list(stok.keys()))
print(list(stok.values()))
print(list(stok.items()))
print("Toplam ürün adedi:", sum(stok.values()))
print("En çok stok:", max(stok.values()))
print("Alfabetik:", sorted(stok))


# %% Bölüm 7 — Aynı anahtar iki kez yazılırsa
notlar = {"Ali": 70, "Ece": 85, "Ali": 90}
print(notlar)
print(len(notlar))


# %% Bölüm 8 — Sözlük kopyalamak: copy()
fiyat = {"çay": 20, "kahve": 45}
indirimli = fiyat.copy()
indirimli["kahve"] = 40
print(fiyat)
print(indirimli)


# %% Bölüm 9 — İç içe yapılar: sözlük içinde liste ve sözlük
ogrenci = {
    "ad": "Elif Kaya",
    "no": 1021,
    "notlar": [85, 72, 90],
    "iletisim": {"tel": "0532 000 11 22", "sehir": "Bursa"},
}
print(ogrenci["notlar"][1])
print(ogrenci["iletisim"]["sehir"])
ogrenci["notlar"].append(95)
print(sum(ogrenci["notlar"]) / len(ogrenci["notlar"]))


# %% Bölüm 10 — Küme (set): tekrarsız elemanlar
sepet = ["elma", "süt", "elma", "ekmek", "süt"]
farkli = set(sepet)
print(farkli)
print(len(farkli))
renkler = {"kırmızı", "mavi"}
renkler.add("yeşil")
renkler.add("mavi")
print(len(renkler), "mavi" in renkler)
renkler.discard("mor")
print(sorted(renkler))


# %% Bölüm 11 — Küme işlemleri: kesişim, birleşim, fark
ali = {"yüzme", "satranç", "müzik", "koşu"}
ece = {"müzik", "resim", "koşu"}
print("Ortak:", sorted(ali & ece))
print("Hepsi:", sorted(ali | ece))
print("Yalnız Ali:", sorted(ali - ece))
print("Yalnız birinde:", sorted(ali ^ ece))


# %% Bölüm 13 — Kümelerle gerçek hayat: tekrar temizleme ve alt küme
epostalar = ["ali@ornek.com", "ece@ornek.com", "ali@ornek.com",
             "can@ornek.com", "ece@ornek.com"]
tekil = sorted(set(epostalar))
print(len(epostalar), "kayıt,", len(tekil), "farklı adres")
print(tekil)
gerekli = {"un", "şeker", "yumurta"}
evde = {"un", "süt", "yumurta", "şeker", "tuz"}
print("Kek yapılabilir mi?", gerekli <= evde)


# %% Uygulama 1 — Telefon rehberi
rehber = {"Ayşe Yılmaz": "0532 111 22 33",
          "Mehmet Demir": "0505 444 55 66"}
rehber["Zeynep Kara"] = "0542 777 88 99"
rehber["Mehmet Demir"] = "0507 123 45 67"
silinen = rehber.pop("Ayşe Yılmaz")
aranan = input("Kimi arıyorsunuz? ").strip().title()
numara = rehber.get(aranan, "rehberde kayıtlı değil")
print(f"{aranan}: {numara}")
print("Kayıt sayısı:", len(rehber))
print("Kişiler:", ", ".join(sorted(rehber)))


# %% Uygulama 2 — Kırtasiye stok kaydı
stok = {"kalem": 120, "defter": 45, "silgi": 60, "cetvel": 12}
fiyat = {"kalem": 7.5, "defter": 32.0, "silgi": 5.0, "cetvel": 18.0}
satilan = {"kalem": 30, "cetvel": 10}

stok["kalem"] -= satilan["kalem"]
stok["cetvel"] -= satilan["cetvel"]
stok["boya"] = 25
fiyat["boya"] = 95.0

print("Toplam ürün adedi:", sum(stok.values()))
print("En az stok:", min(stok, key=stok.get))
print("En pahalı ürün:", max(fiyat, key=fiyat.get))
ciro = satilan["kalem"] * fiyat["kalem"] + satilan["cetvel"] * fiyat["cetvel"]
print(f"Bugünkü ciro: {ciro:.2f} TL")
print("Kalem kalan:", stok["kalem"], "| Cetvel kalan:", stok.get("cetvel"))


# %% Bölüm 12 — min/max ile key=sozluk.get
stok = {"kalem": 90, "cetvel": 2}
print(min(stok))
print(min(stok, key=stok.get))
print(min(stok.values()))


# %% Alıştırma 1 — çözüm
kitap = {"ad": "Kürk Mantolu Madonna",
         "yazar": "Sabahattin Ali",
         "sayfa": 160, "yil": 1943}
print(kitap["yazar"])
kitap["sayfa"] += 20
kitap["okundu"] = True
print(list(kitap.keys()))


# %% Alıştırma 2 — çözüm
sozluk = {"apple": "elma", "book": "kitap",
          "water": "su", "house": "ev"}
kelime = input("Kelime: ").strip().lower()
anlam = sozluk.get(kelime, "bilinmiyor")
print(f"{kelime} → {anlam}")


# %% Alıştırma 3 — çözüm (düzeltilmiş)
fiyat = {"çay": 20, "kahve": 45}
print(fiyat["çay"])
fiyat["su"] = 10
yeni = set()
yeni.add("çay")
print(fiyat, yeni)


# %% Alıştırma 4 — çözüm
python = ["Ali", "Ece", "Can", "Ece"]
excel = ["Can", "Deniz", "Ali"]

p = set(python)
e = set(excel)

print("Python farklı öğrenci:", len(p))
print("Excel farklı öğrenci:", len(e))
print("İki kursta da:", sorted(p & e))
print("Yalnız Python:", sorted(p - e))
print("Toplam farklı öğrenci:", len(p | e))


# %% Ek — Gelecek dersin önizlemesi: koşullar
not_ = 72
if not_ >= 50:
    print("Geçti")
else:
    print("Kaldı")
