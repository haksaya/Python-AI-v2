# =============================================================================
# Python Kursu — Ders 25 (Hafta 13, Gün 1)
# Konu: Web nasıl çalışır, frontend/backend/fullstack, UX ve UI, HTML etiketleri, listeler, tablolar, formlar, semantik yapı, CSS seçiciler, kutu modeli, flexbox, duyarlı tasarım, Bootstrap ızgarası ve bileşenleri — kişisel tanıtım sayfası
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Bu derste HTML ve CSS yazıyoruz. Her hücre, ilgili .html/.css dosyalarını bu .py ile aynı klasöre YAZAR; sonra dosyayı tarayıcıda açın (çift tıklama ya da VS Code 'Live Server').
#   - Bootstrap örnekleri internetten (cdn.jsdelivr.net) yüklenir; internet bağlantısı gerekir.
#   - İsteğe bağlı: terminalde 'python -m http.server 8000' çalıştırıp http://localhost:8000 adresinden de açabilirsiniz.
#   - Sayfalardaki kişi (Deniz Kaya) kurgusaldır; kendi bilgilerinizle değiştirin.
# =============================================================================


# %% Bölüm 0 — Profil resmi (profil.svg) oluştur
from pathlib import Path

PROFIL = """<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="100" fill="#2E6DB4"/>
  <text x="100" y="125" font-size="72" text-anchor="middle" fill="white" font-family="Arial">DK</text>
</svg>"""
Path("profil.svg").write_text(PROFIL, encoding="utf-8")
print("profil.svg yazıldı")


# %% Bölüm 1 — İlk HTML sayfası (ilk_sayfa.html)
from pathlib import Path

dosyalar = {
    "ilk_sayfa.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>İlk sayfam</title>
</head>
<body>
  <h1>Merhaba, Web!</h1>
  <p>Bu benim ilk web sayfam.</p>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 2 — Metin, görsel ve bağlantı (metin.html)
from pathlib import Path

dosyalar = {
    "metin.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Deniz Kaya</title>
</head>
<body>
  <h1>Deniz Kaya</h1>
  <h2>Python öğrencisi</h2>
  <p>Merhaba! <strong>Veri analizi</strong> ve <em>web</em>
     ile ilgileniyorum.<br>İstanbul'da yaşıyorum.</p>
  <img src="profil.svg" alt="Deniz Kaya'nın profil resmi"
       width="120">
  <p>Kodlarım için: <a href="https://github.com">GitHub</a></p>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 3 — Listeler ve tablo (liste_tablo.html)
from pathlib import Path

dosyalar = {
    "liste_tablo.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Listeler ve tablolar</title>
</head>
<body>
  <h2>Becerilerim</h2>
  <ul>
    <li>Python</li>
    <li>Pandas ve Matplotlib</li>
    <li>SQL</li>
  </ul>
  <h2>Bu haftanın planı</h2>
  <ol>
    <li>Ders tekrarı</li>
    <li>Tanıtım sayfası ödevi</li>
  </ol>
  <table border="1">
    <tr><th>Ders</th><th>Konu</th></tr>
    <tr><td>23</td><td>Veri temizleme</td></tr>
    <tr><td>24</td><td>Matplotlib</td></tr>
  </table>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 4 — Form (form.html)
from pathlib import Path

dosyalar = {
    "form.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>İletişim formu</title>
</head>
<body>
  <h2>Bana yazın</h2>
  <form action="#">
    <p><label for="ad">Adınız</label><br>
       <input id="ad" name="ad" type="text"
              placeholder="Ad Soyad" required></p>
    <p><label for="eposta">E-posta</label><br>
       <input id="eposta" name="eposta" type="email"></p>
    <p><label for="mesaj">Mesaj</label><br>
       <textarea id="mesaj" name="mesaj" rows="3"></textarea></p>
    <button type="submit">Gönder</button>
  </form>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 5 — Semantik iskelet (semantik.html)
from pathlib import Path

dosyalar = {
    "semantik.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Semantik iskelet</title>
</head>
<body>
  <header>
    <h1>Deniz Kaya</h1>
    <nav>
      <a href="#hakkimda">Hakkımda</a>
      <a href="#projeler">Projeler</a>
    </nav>
  </header>
  <main>
    <section id="hakkimda"><h2>Başlık</h2><p>İçerik</p></section>
    <section id="projeler"><h2>Başlık</h2><p>İçerik</p></section>
  </main>
  <footer>© 2026 Deniz Kaya</footer>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 6 — İlk CSS: stil.css ve css_ilk.html
from pathlib import Path

dosyalar = {
    "stil.css": """body {
  font-family: Arial, sans-serif;
  background: #f4f6f8;
  color: #222;
  padding: 24px;
}
h1 { color: #2e6db4; }
.vurgu { background: #fff3c4; padding: 4px 8px; }
#altbilgi { color: gray; font-size: 14px; }""",
    "css_ilk.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CSS ile stil</title>
  <link rel="stylesheet" href="stil.css">
</head>
<body>
  <h1>Deniz Kaya</h1>
  <p class="vurgu">Python ve veri analizi öğreniyorum.</p>
  <p>Bu paragrafın özel bir stili yok.</p>
  <p id="altbilgi">Son güncelleme: Ekim 2026</p>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 7 — Kutu modeli (kutu.html)
from pathlib import Path

dosyalar = {
    "kutu.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kutu modeli</title>
  <style>
  body { font-family: Arial, sans-serif; background: #eef1f5; }
  .kart {
    width: 260px;
    padding: 20px;
    border: 3px solid #2e6db4;
    border-radius: 12px;
    margin: 16px;
    background: white;
  }
  </style>
</head>
<body>
  <div class="kart">
    <h3>Bütçe paneli</h3>
    <p>Matplotlib ile 2×2 grafik.</p>
  </div>
  <div class="kart">
    <h3>Ev ilanları</h3>
    <p>Pandas ile veri temizleme.</p>
  </div>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 8 — Flexbox (flex.html)
from pathlib import Path

dosyalar = {
    "flex.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flexbox</title>
  <style>
  body { font-family: Arial, sans-serif; text-align: center; }
  .satir {
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
  }
  .kutu {
    background: #2e6db4;
    color: white;
    padding: 24px;
    border-radius: 10px;
    width: 140px;
    text-align: center;
  }
  </style>
</head>
<body>
  <h2>Becerilerim</h2>
  <div class="satir">
    <div class="kutu">Python</div>
    <div class="kutu">Pandas</div>
    <div class="kutu">SQL</div>
    <div class="kutu">HTML/CSS</div>
  </div>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 9 — Bootstrap ızgarası ve kartlar (bootstrap.html)
from pathlib import Path

dosyalar = {
    "bootstrap.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bootstrap</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container py-4">
  <h1 class="mb-3">Projelerim</h1>
  <div class="row g-3">
    <div class="col-md-4">
      <div class="card h-100"><div class="card-body">
        <h5 class="card-title">Bütçe paneli</h5>
        <p class="card-text">Matplotlib ile 2×2 grafik.</p>
        <a href="#" class="btn btn-primary">İncele</a>
      </div></div>
    </div>
    <div class="col-md-4">
      <div class="card h-100"><div class="card-body">
        <h5 class="card-title">Ev ilanları</h5>
        <p class="card-text">Pandas ile veri temizleme.</p>
        <a href="#" class="btn btn-primary">İncele</a>
      </div></div>
    </div>
    <div class="col-md-4">
      <div class="card h-100"><div class="card-body">
        <h5 class="card-title">Yorum analizi</h5>
        <p class="card-text">Streamlit ile duygu analizi uygulaması.</p>
        <a href="#" class="btn btn-primary">İncele</a>
      </div></div>
    </div>
  </div>
</div>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 10 — Bootstrap bileşenleri (bilesenler.html)
from pathlib import Path

dosyalar = {
    "bilesenler.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bootstrap bileşenleri</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand bg-dark" data-bs-theme="dark">
  <div class="container">
    <a class="navbar-brand" href="#">Deniz Kaya</a>
    <div class="navbar-nav">
      <a class="nav-link" href="#hakkimda">Hakkımda</a>
      <a class="nav-link" href="#projeler">Projeler</a>
    </div>
  </div>
</nav>
<div class="container py-4">
  <div class="alert alert-success">Mesajınız gönderildi!</div>
  <button class="btn btn-primary">Birincil</button>
  <button class="btn btn-outline-secondary">İkincil</button>
  <span class="badge text-bg-warning">Yeni</span>
</div>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Bölüm 11 — Python ile HTML üretmek (projeler.html)
from pathlib import Path

projeler = [
    {"ad": "Bütçe paneli", "ders": 24, "ozet": "Matplotlib ile 2×2 grafik"},
    {"ad": "Ev ilanları", "ders": 23, "ozet": "Pandas ile veri temizleme"},
    {"ad": "Yorum analizi", "ders": 13, "ozet": "Streamlit uygulaması"},
]
satirlar = ""
for p in projeler:
    satirlar += f"<li><b>{p['ad']}</b> (Ders {p['ders']}): {p['ozet']}</li>\n"

sayfa = f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><title>Projeler</title></head>
<body><h1>Projelerim ({len(projeler)})</h1><ul>
{satirlar}</ul></body></html>"""
Path("projeler.html").write_text(sayfa, encoding="utf-8")
print("projeler.html yazıldı")


# %% Uygulama — Kişisel tanıtım sayfası (tanitim.html)
from pathlib import Path

dosyalar = {
    "tanitim.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Deniz Kaya — Python öğrencisi</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    .hero { background: linear-gradient(135deg, #16233a, #2e6db4); color: white; }
    .hero img { width: 140px; border-radius: 50%; border: 4px solid white; }
    section { scroll-margin-top: 70px; }
  </style>
</head>
<body>
<nav class="navbar navbar-expand bg-dark sticky-top" data-bs-theme="dark">
  <div class="container">
    <a class="navbar-brand" href="#">Deniz Kaya</a>
    <div class="navbar-nav">
      <a class="nav-link" href="#hakkimda">Hakkımda</a>
      <a class="nav-link" href="#projeler">Projeler</a>
      <a class="nav-link" href="#iletisim">İletişim</a>
    </div>
  </div>
</nav>

<header class="hero text-center py-5">
  <img src="profil.svg" alt="Profil fotoğrafı">
  <h1 class="mt-3">Merhaba, ben Deniz</h1>
  <p class="lead">Python, veri analizi ve web geliştirme öğreniyorum.</p>
  <a href="#projeler" class="btn btn-light btn-lg">Projelerimi gör</a>
</header>

<main class="container py-5">
  <section id="hakkimda" class="mb-5">
    <h2>Hakkımda</h2>
    <p>İstanbul'da yaşıyorum. Verilerden hikâye çıkarmayı ve bunları web'de paylaşmayı seviyorum.</p>
    <span class="badge text-bg-primary">Python</span>
    <span class="badge text-bg-primary">Pandas</span>
    <span class="badge text-bg-primary">Matplotlib</span>
    <span class="badge text-bg-secondary">SQL</span>
    <span class="badge text-bg-secondary">HTML/CSS</span>
  </section>

  <section id="projeler" class="mb-5">
    <h2>Projelerim</h2>
    <div class="row g-3">
    <div class="col-md-4">
      <div class="card h-100"><div class="card-body">
        <h5 class="card-title">Bütçe paneli</h5>
        <p class="card-text">Altı aylık harcamaları Matplotlib ile 2×2 panelde inceledim.</p>
        <a href="#" class="btn btn-primary">İncele</a>
      </div></div>
    </div>
    <div class="col-md-4">
      <div class="card h-100"><div class="card-body">
        <h5 class="card-title">Ev ilanları</h5>
        <p class="card-text">Kirli ilan verisini Pandas ile temizleyip analiz ettim.</p>
        <a href="#" class="btn btn-success">İncele</a>
      </div></div>
    </div>
    <div class="col-md-4">
      <div class="card h-100"><div class="card-body">
        <h5 class="card-title">Yorum analizi</h5>
        <p class="card-text">Ürün yorumlarının duygusunu ölçen Streamlit uygulaması.</p>
        <a href="#" class="btn btn-warning">İncele</a>
      </div></div>
    </div>
    </div>
  </section>

  <section id="iletisim">
    <h2>İletişim</h2>
    <form action="#" class="row g-2" style="max-width: 520px">
      <div class="col-12"><input class="form-control" placeholder="Adınız" required></div>
      <div class="col-12"><input class="form-control" type="email" placeholder="E-posta"></div>
      <div class="col-12"><textarea class="form-control" rows="3" placeholder="Mesajınız"></textarea></div>
      <div class="col-12"><button class="btn btn-primary">Gönder</button></div>
    </form>
  </section>
</main>

<footer class="bg-light text-center py-3">© 2026 Deniz Kaya · Python Kursu</footer>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 1 — çözüm (favoriler.html)
from pathlib import Path

dosyalar = {
    "favoriler.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Favorilerim</title>
</head>
<body>
  <h1>Favori kitaplarım</h1>
  <ol>
    <li><a href="https://tr.wikipedia.org/wiki/Simyacı">Simyacı</a></li>
    <li><a href="https://tr.wikipedia.org/wiki/Küçük_Prens">Küçük Prens</a></li>
    <li><a href="https://tr.wikipedia.org/wiki/Saatleri_Ayarlama_Enstitüsü">
        Saatleri Ayarlama Enstitüsü</a></li>
  </ol>
  <img src="profil.svg" alt="Profil resmim" width="100">
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 2 — çözüm (kartvizit.html + kartvizit.css)
from pathlib import Path

dosyalar = {
    "kartvizit.css": """body { font-family: Arial, sans-serif; background: #eef1f5; }
.kartvizit {
  width: 320px;
  margin: 40px auto;
  padding: 24px;
  background: white;
  border-left: 6px solid #2e6db4;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.kartvizit h2 { color: #2e6db4; margin: 0 0 4px; }
.kartvizit p { color: #666; margin: 4px 0; }""",
    "kartvizit.html": """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kartvizit</title>
  <link rel="stylesheet" href="kartvizit.css">
</head>
<body>
  <div class="kartvizit">
    <h2>Deniz Kaya</h2>
    <p>Python geliştirici adayı</p>
    <p>deniz@ornek.com</p>
    <p>İstanbul</p>
  </div>
</body>
</html>""",
}
for ad, icerik in dosyalar.items():
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 3 — çözüm (kartlar.html)
from pathlib import Path

projeler = [
    {"ad": "Bütçe paneli", "aciklama": "Matplotlib panosu", "renk": "primary"},
    {"ad": "Ev ilanları", "aciklama": "Pandas ile temizlik", "renk": "success"},
    {"ad": "Yorum analizi", "aciklama": "Streamlit uygulaması", "renk": "warning"},
]
kartlar = ""
for p in projeler:
    kartlar += f"""
    <div class="col-md-4">
      <div class="card text-bg-{p['renk']} h-100"><div class="card-body">
        <h5 class="card-title">{p['ad']}</h5>
        <p class="card-text">{p['aciklama']}</p>
      </div></div>
    </div>"""
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
sayfa = f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><title>Kartlar</title>
<link href="{BS}" rel="stylesheet"></head>
<body><div class="container py-4"><h1>Projelerim</h1>
<div class="row g-3">{kartlar}
</div></div></body></html>"""
Path("kartlar.html").write_text(sayfa, encoding="utf-8")
print(len(projeler), "kart yazıldı → kartlar.html")
