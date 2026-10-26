# =============================================================================
# Python Kursu — Ders 1 (Hafta 1, Gün 1)
# Konu: Python'a Giriş, Kurulum, VS Code, Jupyter Notebook ve Google Colab
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır.
#   - VS Code'da hücrenin üstündeki "Run Cell" yazısına tıklayarak
#     yalnızca o hücreyi çalıştırabilirsiniz (Jupyter eklentisi gerekir).
#   - Ya da dosyanın tamamını sağ üstteki ▶ (Run Python File) ile çalıştırın.
#   - Bu dersin kodları için ek kurulum (pip install) GEREKMEZ.
# =============================================================================


# %% Bölüm 1 — Hangi Python sürümünü kullanıyorum?
# sys modülü Python'un kendisi hakkında bilgi verir (modülleri Ders 10'da işleyeceğiz).
import sys

print("Python sürümü:", sys.version)
print("Python'un yeri:", sys.executable)


# %% Bölüm 2 — İlk programımız
# print() ekrana yazı yazdırır. Yazıyı (metni) tırnak içine alırız.
print("Merhaba Dünya!")
print("Python kursuna hoş geldiniz.")


# %% Bölüm 3 — print() ile birden fazla değer
# Virgülle ayırdığımız değerler arasına print() otomatik bir boşluk koyar.
print("Kurs süresi:", 96, "saat")
print("Ders sayısı:", 32)

# sep: değerlerin arasına ne konacağını belirler (varsayılan: boşluk)
print("2026", "10", "25", sep="-")

# end: satırın sonuna ne konacağını belirler (varsayılan: alt satıra geç)
print("Yükleniyor", end="...")
print("tamam!")


# %% Bölüm 4 — Python bir hesap makinesidir
print(2 + 3)        # toplama      -> 5
print(10 - 4)       # çıkarma      -> 6
print(6 * 7)        # çarpma       -> 42
print(7 / 2)        # bölme        -> 3.5 (sonuç hep ondalıklı)
print(7 // 2)       # tam bölme    -> 3
print(7 % 2)        # kalan (mod)  -> 1
print(2 ** 10)      # üs alma      -> 1024
print((2 + 3) * 4)  # parantez önce -> 20


# %% Bölüm 5 — Yorum satırları
# Bu satır bir yorumdur; Python bunu çalıştırmaz.
# Yorumlar, kodu okuyan insanlar (ve gelecekteki siz!) içindir.

print("Bu satır çalışır")   # satırın sonuna da yorum yazılabilir
# print("Bu satır çalışmaz, çünkü başında # var")

# VS Code kısayolu: satırı seçip Ctrl + /  (macOS: Cmd + /) ile yorum yap/kaldır.


# %% Bölüm 6 — Sık yapılan hatalar (hepsini düzeltilmiş halde görüyorsunuz)
# Hatalı halleri derste tek tek denenecek; burada doğru halleri var.

# Hata 1: Tırnağı kapatmamak
#   print("Merhaba)          -> SyntaxError: unterminated string literal
print("Merhaba")

# Hata 2: Büyük harf kullanmak
#   Print("Merhaba")         -> NameError: name 'Print' is not defined
print("Merhaba")

# Hata 3: Satır başında gereksiz boşluk
#      print("Merhaba")      -> IndentationError: unexpected indent
print("Merhaba")

# Hata 4: Parantezi kapatmamak
#   print("Merhaba"          -> SyntaxError: '(' was never closed
print("Merhaba")

# Hata 5: Sıfıra bölmek
#   print(10 / 0)            -> ZeroDivisionError: division by zero
print(10 / 2)


# %% Bölüm 7 — Gerçek hayattan uygulama: Kahve dükkanı fişi
# Henüz değişken bilmiyoruz; yalnızca print() ve aritmetik kullanıyoruz.
# "=" * 32 ifadesi "=" işaretini 32 kez yan yana yazar (ayrıntısı Ders 3'te).
print("=" * 32)
print("KÖŞE KAHVECİSİ")
print("=" * 32)
print("2 x Türk kahvesi:", 2 * 85, "TL")
print("1 x Simit:", 1 * 30, "TL")
print("3 x Çay:", 3 * 25, "TL")
print("-" * 32)
print("TOPLAM:", 2 * 85 + 1 * 30 + 3 * 25, "TL")
print("Kişi başı:", (2 * 85 + 1 * 30 + 3 * 25) / 2, "TL")
print("=" * 32)
print("Teşekkür ederiz!")


# =============================================================================
# SINIF İÇİ ALIŞTIRMALARIN ÇÖZÜMLERİ
# =============================================================================

# %% Alıştırma 1 (kolay) — Kendinizi tanıtın
print("Adım: Ayşe")
print("Şehrim: İstanbul")
print("Python'u veri analizi için öğreniyorum.")


# %% Alıştırma 2 (kolay-orta) — Python ile hesap
print("Kurs toplam dakika:", 96 * 60)
print("Bir dersteki dakika:", 3 * 60)
print("Haftalık ders saati:", 2 * 3)
print("İki blok toplamı:", 2 * 75)


# %% Alıştırma 3 (orta) — Hata avı (düzeltilmiş hali)
# Hatalı hali:
#   Print("Python")
#   print("Kursuna hoş geldiniz)
#     print(5 + 3
print("Python")
print("Kursuna hoş geldiniz")
print(5 + 3)


# %% Alıştırma 4 (zor) — İndirimli market fişi
# 2 kg elma (kg'ı 45 TL), 3 süt (tanesi 38 TL), 1 ekmek (15 TL); toplamda %10 indirim
print("=" * 30)
print("MAHALLE MARKETİ")
print("=" * 30)
print("2 kg Elma:", 2 * 45, "TL")
print("3 x Süt:", 3 * 38, "TL")
print("1 x Ekmek:", 1 * 15, "TL")
print("-" * 30)
print("Ara toplam:", 2 * 45 + 3 * 38 + 1 * 15, "TL")
print("İndirim (%10):", (2 * 45 + 3 * 38 + 1 * 15) * 10 / 100, "TL")
print("ÖDENECEK:", (2 * 45 + 3 * 38 + 1 * 15) * 90 / 100, "TL")
print("=" * 30)
print("Fiş tarihi:", end=" ")
print(25, 10, 2026, sep="/")


# =============================================================================
# EKLER
# =============================================================================

# %% Ek A — "# %%" hücreleri ve hücre sırası (Jupyter bölümü)
# Önce aşağıdaki "Ek A.1" hücresini, sonra "Ek A.2"yi çalıştırın.
# Ek A.2'yi Ek A.1'den ÖNCE çalıştırırsanız: NameError: name 'sys' is not defined
# (Dosyayı ▶ ile baştan sona çalıştırınca sorun olmaz; sys en üstte zaten yüklendi.)

# %% Ek A.1
import sys

# %% Ek A.2
print("Python sürümü:", sys.version)

# %% Ek A.3
print("Kurs süresi:", 96 * 60, "dakika")


# %% Ek B — Google Colab / notebook hücresi
# Aşağıdaki ilk satır YALNIZCA notebook'larda (Colab veya VS Code .ipynb) çalışır.
# Başındaki "!" satırı terminale gönderir. Normal .py dosyasında SyntaxError verdiği
# için burada yorum olarak duruyor; Colab'a kopyalarken baştaki "# " kısmını silin.
# !python --version
print("Merhaba Colab!")


# %% Ek C — Gelecek dersin önizlemesi: değişkenler
cay_fiyati = 25
cay_adedi = 3
print("Çay:", cay_fiyati * cay_adedi, "TL")
