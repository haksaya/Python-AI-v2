# =============================================================================
# Python Kursu — Ders 12 (Hafta 6, Gün 2)
# Konu: Streamlit kurulumu, web tabanlı arayüz, Streamlit metotları; döviz kuru gösterici uygulaması
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - Bu dosya bir STREAMLIT uygulamasıdır. Terminalde: streamlit run ders12_streamlit_temelleri.py
#   - Bölümler '# ----' satırlarıyla ayrılmıştır; hepsi aynı sayfada alt alta görünür.
#   - Kurulum (sanal ortam etkinken): python -m pip install streamlit requests
#   - Döviz uygulaması ayrı dosyadadır: streamlit run ders12_doviz_uygulamasi.py (internet gerekir).
# =============================================================================


# ---- Başlangıç
import streamlit as st

st.set_page_config(page_title="Ders 12 — Streamlit temelleri")
st.caption("Python Kursu · Ders 12 · Bütün örnekler bölüm bölüm")


# ---- Bölüm 1 — İlk uygulama
st.header("Bölüm 1 — İlk uygulama")
st.title("Merhaba Streamlit")
st.write("Bu benim ilk web uygulamam.")
ad = st.text_input("Adınız")
if ad:
    st.write(f"Hoş geldin, {ad}!")


# ---- Bölüm 2 — Metin bileşenleri
st.header("Bölüm 2 — Metin bileşenleri")
st.title("Başlık: st.title")
st.header("Bölüm başlığı: st.header")
st.subheader("Alt başlık: st.subheader")
st.write("st.write metin, sayı, liste… yazar:", 42)
st.markdown("**Kalın**, *italik* ve `kod`")
st.caption("Küçük açıklama: st.caption")
st.code('print("Merhaba")', language="python")


# ---- Bölüm 3 — Tablo ve metrik
st.header("Bölüm 3 — Tablo ve metrik")
urunler = [
    {"Ürün": "Kalem", "Fiyat": 7.5, "Stok": 90},
    {"Ürün": "Defter", "Fiyat": 32.0, "Stok": 45},
    {"Ürün": "Silgi", "Fiyat": 5.0, "Stok": 60},
]
st.subheader("Stok tablosu")
st.dataframe(urunler, hide_index=True)
toplam = sum(u["Stok"] for u in urunler)
st.metric("Toplam stok", toplam, delta=-30)


# ---- Bölüm 4 — Girdi bileşenleri
st.header("Bölüm 4 — Girdi bileşenleri")
ad = st.text_input("Ad", "Ayşe")
yas = st.number_input("Yaş", min_value=0, max_value=120, value=34)
puan = st.slider("Memnuniyet (1-10)", 1, 10, 8)
sehir = st.selectbox("Şehir", ["İstanbul", "Ankara", "İzmir"])
uyelik = st.radio("Üyelik", ["Standart", "Premium"], horizontal=True)
onay = st.checkbox("Koşulları okudum", value=True)
st.write(ad, yas, puan, sehir, uyelik, onay)


# ---- Bölüm 5 — Düğme ve mesajlar
st.header("Bölüm 5 — Düğme ve mesajlar")
tutar = st.number_input("Tutar (TL)", min_value=0.0, value=1250.0, step=50.0)
if st.button("KDV'li fiyatı hesapla"):
    st.success(f"KDV dahil: {tutar * 1.20:,.2f} TL")
st.info("Bilgi mesajı: st.info")
st.warning("Uyarı mesajı: st.warning")
st.error("Hata mesajı: st.error")


# ---- Bölüm 6 — Sayfa düzeni
st.header("Bölüm 6 — Sayfa düzeni")
st.sidebar.header("Ayarlar")
sinif = st.sidebar.selectbox("Sınıf", ["10-A", "10-B"])
st.title(f"{sinif} sınıf panosu")
sol, sag = st.columns(2)
sol.metric("Ortalama not", 82.5, 3.2)
sag.metric("Devamsızlık", "2 gün", -1)
sekme1, sekme2 = st.tabs(["Özet", "Notlar"])
with sekme1:
    st.write("Bu dönem sınıf ortalaması yükseldi.")
with sekme2:
    st.write("Veli toplantısı Cuma günü.")
with st.expander("Ayrıntılar"):
    st.write("Açılır kutunun içeriği")


# ---- Bölüm 7 — Çizgi ve sütun grafiği
st.header("Bölüm 7 — Çizgi ve sütun grafiği")
adimlar = {"Gün": [1, 2, 3, 4, 5, 6, 7],
           "Adım": [6540, 8210, 4300, 10250, 7700, 12100, 5050]}
st.subheader("Haftalık adım sayısı")
st.line_chart(adimlar, x="Gün", y="Adım")
st.bar_chart(adimlar, x="Gün", y="Adım")


# ---- Bölüm 8 — session_state ile sayaç
st.header("Bölüm 8 — session_state ile sayaç")
if "sayac" not in st.session_state:
    st.session_state.sayac = 0
if st.button("Bir artır"):
    st.session_state.sayac += 1
st.write("Sayaç:", st.session_state.sayac)


# ---- Bölüm 9 — Uygulama 2: Not hesaplayıcı
st.header("Bölüm 9 — Uygulama 2: Not hesaplayıcı")
def harf_notu(puan):
    for sinir, harf in [(90, "AA"), (85, "BA"), (80, "BB"), (75, "CB"),
                        (70, "CC"), (65, "DC"), (60, "DD"), (50, "FD")]:
        if puan >= sinir:
            return harf
    return "FF"


st.title("Not Hesaplayıcı")
vize = st.slider("Vize", 0, 100, 60)
final = st.slider("Final", 0, 100, 75)
oran = st.select_slider("Vize ağırlığı (%)", [30, 40, 50], 40)
ortalama = vize * oran / 100 + final * (100 - oran) / 100
sol, sag = st.columns(2)
sol.metric("Ortalama", f"{ortalama:.1f}")
sag.metric("Harf notu", harf_notu(ortalama))
if ortalama >= 60:
    st.success("Tebrikler, dersi geçtiniz.")
else:
    st.error("Maalesef dersten kaldınız.")


# ---- Alıştırma 1 — çözüm
st.header("Alıştırma 1 — çözüm")
boy = st.number_input("Boy (m)", 1.0, 2.5, 1.75, step=0.01)
kilo = st.number_input("Kilo (kg)", 20.0, 250.0, 70.0, step=0.5)
vki = kilo / boy ** 2
st.metric("VKİ", f"{vki:.2f}")
if vki < 18.5:
    st.warning("Zayıf")
elif vki < 25:
    st.success("Normal")
elif vki < 30:
    st.warning("Fazla kilolu")
else:
    st.error("Obez")


# ---- Alıştırma 2 — çözüm
st.header("Alıştırma 2 — çözüm")
sozluk = {"apple": "elma", "book": "kitap", "water": "su", "house": "ev"}
st.sidebar.write("Kelime sayısı:", len(sozluk))
secim = st.selectbox("Kelime", sorted(sozluk))
st.subheader(f"{secim} → {sozluk[secim]}")


# ---- Alıştırma 3 — çözüm
st.header("Alıştırma 3 — çözüm")
if "gorevler" not in st.session_state:
    st.session_state.gorevler = []

gorev = st.text_input("Yeni görev")
sol, sag = st.columns(2)
if sol.button("Ekle") and gorev.strip():
    st.session_state.gorevler.append(gorev.strip())
if sag.button("Temizle"):
    st.session_state.gorevler = []

for i, g in enumerate(st.session_state.gorevler, start=1):
    st.write(f"{i}. {g}")
