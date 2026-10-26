"""Metin araçları: Ders 9'da yazdığımız fonksiyonlar."""


def tr_buyuk(metin):
    """Türkçe kurallarıyla büyük harf: i → İ, ı → I."""
    return metin.replace("i", "İ").replace("ı", "I").upper()


def tr_kucuk(metin):
    """Türkçe kurallarıyla küçük harf: I → ı, İ → i."""
    return metin.replace("I", "ı").replace("İ", "i").lower()


def ad_duzelt(ad):
    """'  İLKER   ışık ' → 'İlker Işık'"""
    duzgun = []
    for k in ad.split():
        duzgun.append(tr_buyuk(k[0]) + tr_kucuk(k[1:]))
    return " ".join(duzgun)


if __name__ == "__main__":
    print(ad_duzelt("  ayşe   YILMAZ "))
