# Python Kursu — Ders 13 Mini Proje: Türkçe Yorum Analizi
# Çalıştırma: streamlit run ders13_yorum_analizi_app.py
# Gerekenler: python -m pip install streamlit transformers torch  ·  ilk çalıştırmada internet

import streamlit as st
from transformers import pipeline

MODEL = "savasy/bert-base-turkish-sentiment-cased"
st.set_page_config(page_title="Yorum Analizi")


@st.cache_resource
def model_yukle():
    return pipeline("sentiment-analysis", model=MODEL)


def etiket_cevir(etiket):
    etiket = etiket.lower()
    if etiket in ("positive", "label_1"):
        return "Olumlu"
    if etiket in ("negative", "label_0"):
        return "Olumsuz"
    return etiket


st.title("Türkçe Yorum Analizi")
st.caption(f"Model: {MODEL} (Hugging Face) · Sonuçlar tahmindir.")
with st.spinner("Model yükleniyor…"):
    analiz = model_yukle()

if "gecmis" not in st.session_state:
    st.session_state.gecmis = []

with st.form("yorum_formu", clear_on_submit=True):
    yorum = st.text_area("Yorumunuz", placeholder="Ör. Ürün beklediğimden iyi çıktı.")
    gonder = st.form_submit_button("Analiz et")

if gonder and yorum.strip():
    sonuc = analiz(yorum)[0]
    duygu = etiket_cevir(sonuc["label"])
    guven = sonuc["score"]
    st.session_state.gecmis.insert(0, {"Yorum": yorum, "Duygu": duygu, "Güven": round(guven, 3)})
    if duygu == "Olumlu":
        st.success(f"{duygu} (güven: {guven:.0%})")
    else:
        st.error(f"{duygu} (güven: {guven:.0%})")

if st.session_state.gecmis:
    st.subheader("Bu oturumdaki analizler")
    st.dataframe(st.session_state.gecmis, hide_index=True)
