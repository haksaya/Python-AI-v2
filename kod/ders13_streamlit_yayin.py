# =============================================================================
# Python Kursu — Ders 13 (Hafta 7, Gün 1)
# Konu: Streamlit formları ve dosya yükleme, Hugging Face transformers ile Türkçe duygu analizi (CPU), GitHub + Streamlit Community Cloud ile yayınlama
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - Bu dosya bir STREAMLIT uygulamasıdır. Terminalde: streamlit run ders13_streamlit_yayin.py
#   - Bölümler '# ----' satırlarıyla ayrılmıştır; hepsi aynı sayfada alt alta görünür.
#   - Kurulum (sanal ortam etkinken): python -m pip install streamlit transformers torch
#   - İlk çalıştırmada model (~440 MB) Hugging Face'ten indirilir; internet gerekir.
#   - Yayınlanacak uygulama ayrı dosyadadır: ders13_yorum_analizi_app.py (+ requirements.txt).
# =============================================================================


# ---- Başlangıç
import streamlit as st

st.set_page_config(page_title="Ders 13 — Streamlit 2")
st.caption("Python Kursu · Ders 13 · Formlar, dosya yükleme ve duygu analizi")


# ---- Bölüm 1 — Form
st.header("Bölüm 1 — Form")
with st.form("kayit_formu", clear_on_submit=True):
    ad = st.text_input("Ad")
    yas = st.number_input("Yaş", 0, 120, 30)
    gonder = st.form_submit_button("Kaydet")
if gonder and ad:
    st.success(f"{ad} ({yas}) kaydedildi.")


# ---- Bölüm 2 — Dosya yükleme
st.header("Bölüm 2 — Dosya yükleme")
dosya = st.file_uploader("Yorum dosyası (.txt)", type="txt")
if dosya is not None:
    metin = dosya.read().decode("utf-8")
    satirlar = [s.strip() for s in metin.splitlines() if s.strip()]
    st.write(f"{len(satirlar)} yorum okundu.")
    st.dataframe({"Yorum": satirlar})


# ---- Bölüm 3 — İlk model: pipeline (sonuçlar sayfaya yazılır)
from transformers import pipeline

analiz_deneme = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")
for yorum in ["Ürün çok kaliteli, herkese tavsiye ederim.", "Kargo çok geç geldi, hiç memnun kalmadım."]:
    sonuc = analiz_deneme(yorum)[0]
    st.write(sonuc["label"], round(sonuc["score"], 3), "|", yorum)


# ---- Bölüm 4 — Mini proje: yorum analizi (tam hali ders13_yorum_analizi_app.py dosyasında)
st.info('Tam uygulama için: streamlit run ders13_yorum_analizi_app.py')


# ---- Bölüm 5 — Toplu yorum analizi (dosya yükleme + model)
from transformers import pipeline


@st.cache_resource
def model_yukle_toplu():
    return pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")


def etiket_cevir_toplu(etiket):
    etiket = etiket.lower()
    if etiket in ("positive", "label_1"):
        return "Olumlu"
    if etiket in ("negative", "label_0"):
        return "Olumsuz"
    return etiket


st.header("Toplu Yorum Analizi")
dosya = st.file_uploader("Her satıra bir yorum (.txt)", type="txt", key="toplu")
if dosya is not None:
    yorumlar = [s.strip() for s in dosya.read().decode("utf-8").splitlines() if s.strip()]
    sonuclar = model_yukle_toplu()(yorumlar)
    tablo = [{"Yorum": y, "Duygu": etiket_cevir_toplu(s["label"])} for y, s in zip(yorumlar, sonuclar)]
    olumlu = sum(1 for t in tablo if t["Duygu"] == "Olumlu")
    sol, sag = st.columns(2)
    sol.metric("Olumlu", olumlu)
    sag.metric("Olumsuz", len(tablo) - olumlu)
    st.dataframe(tablo, hide_index=True)


# ---- Alıştırma 1–2 — çözüm (model kısmı çıkarıldı)
st.header("Alıştırma 1–2 — çözüm (model kısmı çıkarıldı)")
if "gecmis" not in st.session_state:
    st.session_state.gecmis = [{"Duygu": "Olumlu"},
                               {"Duygu": "Olumsuz"},
                               {"Duygu": "Olumlu"}]

ornek = None
if st.button("Örnek: olumlu"):
    ornek = "Ürün çok kaliteli, herkese tavsiye ederim."
if st.button("Örnek: olumsuz"):
    ornek = "Kargo çok geç geldi, hiç memnun kalmadım."
if ornek:
    st.write("Analiz edilecek:", ornek)

olumlu = sum(1 for k in st.session_state.gecmis if k["Duygu"] == "Olumlu")
st.sidebar.metric("Olumlu", olumlu)
st.sidebar.metric("Olumsuz", len(st.session_state.gecmis) - olumlu)


# ---- Alıştırma 3 — çözüm
st.header("Alıştırma 3 — çözüm")
import json

tablo = [{"Yorum": "Ürün çok kaliteli", "Duygu": "Olumlu"},
         {"Yorum": "Kargo geç geldi", "Duygu": "Olumsuz"}]
metin = json.dumps(tablo, ensure_ascii=False, indent=2)
st.download_button("Sonuçları indir (JSON)", data=metin,
                   file_name="sonuclar.json",
                   mime="application/json")
