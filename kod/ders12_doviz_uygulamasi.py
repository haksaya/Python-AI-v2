# Python Kursu — Ders 12 Uygulama 1: Döviz Kuru Gösterici
# Çalıştırma (sanal ortam etkinken): streamlit run ders12_doviz_uygulamasi.py
# Gerekenler: python -m pip install streamlit requests   ·   İnternet bağlantısı

import requests
import streamlit as st
import xml.etree.ElementTree as ET

TCMB_URL = "https://www.tcmb.gov.tr/kurlar/today.xml"


@st.cache_data(ttl=3600)
def tcmb_kurlari():
    """TCMB'nin bugünkü kurlarını {kod: (isim, döviz satış)} olarak döndürür."""
    yanit = requests.get(TCMB_URL, timeout=10)
    yanit.raise_for_status()
    kok = ET.fromstring(yanit.content)
    kurlar = {}
    for doviz in kok.findall("Currency"):
        satis = doviz.find("ForexSelling").text
        if satis:
            birim = int(doviz.find("Unit").text)
            isim = doviz.find("Isim").text
            kurlar[doviz.get("Kod")] = (isim, float(satis) / birim)
    return kok.get("Tarih"), kurlar


st.title("Döviz Kuru Gösterici")
try:
    tarih, kurlar = tcmb_kurlari()
except requests.exceptions.RequestException:
    st.error("TCMB'ye ulaşılamadı. İnternet bağlantınızı kontrol edin.")
    st.stop()

st.caption(f"Kaynak: TCMB gösterge niteliğindeki kurlar · Bülten: {tarih}")
kod = st.selectbox("Döviz", sorted(kurlar))
isim, kur = kurlar[kod]
miktar = st.number_input(f"Miktar ({kod})", min_value=0.0, value=100.0, step=10.0)
sol, sag = st.columns(2)
sol.metric(f"1 {kod}", f"{kur:.4f} TL")
sag.metric(f"{miktar:g} {kod}", f"{miktar * kur:,.2f} TL")
st.subheader("Bütün kurlar")
tablo = [{"Kod": k, "Döviz": v[0], "Satış (TL)": round(v[1], 4)} for k, v in kurlar.items()]
st.dataframe(tablo, hide_index=True)
