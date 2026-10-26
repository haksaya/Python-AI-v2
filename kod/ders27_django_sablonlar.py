# =============================================================================
# Python Kursu — Ders 27 (Hafta 14, Gün 1)
# Konu: render ve bağlam (context), şablon dili ({{ }}, {% for %}, {% if %}, filtreler), şablon kalıtımı (extends, block), Bootstrap ile base.html, statik dosyalar, URL parametreleri, get_object_or_404, {% url %}, Kategori modeli ve ForeignKey, ilişkili sorgular, context processor — blog listesi ve detay sayfaları
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Ders 26'daki blog_projesi klasöründe, sanal ortam etkinken çalışın (ya da blog_ders26.zip'i açın).
#   - Hücreler şablon, view, URL ve model dosyalarını yazar; makemigrations/migrate komutlarını çalıştırır.
#   - Sunucu: python manage.py runserver → http://127.0.0.1:8000  (Bootstrap internetten yüklenir)
#   - Örnek yazılar kurgusaldır; admin'den kendi yazılarınızı ekleyin.
# =============================================================================


# %% Bölüm 0 — Ders 26 projesi yoksa kur (bir kez)
import os
import subprocess
import sys
from pathlib import Path

# Önceki dersin projesi bu klasörde yoksa onu sıfırdan kurar (varsa hiçbir şey yapmaz).
ASAMALAR = {26: {'sitem/urls.py': 'from django.contrib import admin\nfrom django.urls import include, path\n\nurlpatterns = [\n    path("admin/", admin.site.urls),\n    path("", include("blog.urls")),\n]\n', 'blog/__init__.py': '', 'blog/apps.py': 'from django.apps import AppConfig\n\n\nclass BlogConfig(AppConfig):\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "blog"\n    verbose_name = "Blog"\n', 'blog/models.py': 'from django.db import models\n\n\nclass Yazi(models.Model):\n    baslik = models.CharField("Başlık", max_length=200)\n    icerik = models.TextField("İçerik")\n    olusturma = models.DateTimeField("Oluşturulma", auto_now_add=True)\n    yayinda = models.BooleanField("Yayında", default=False)\n\n    class Meta:\n        verbose_name = "Yazı"\n        verbose_name_plural = "Yazılar"\n        ordering = ["-olusturma"]\n\n    def __str__(self):\n        return self.baslik\n', 'blog/admin.py': 'from django.contrib import admin\n\nfrom .models import Yazi\n\n\n@admin.register(Yazi)\nclass YaziAdmin(admin.ModelAdmin):\n    list_display = ("baslik", "yayinda", "olusturma")\n    list_filter = ("yayinda",)\n    search_fields = ("baslik", "icerik")\n', 'blog/views.py': 'from django.http import HttpResponse\n\nfrom .models import Yazi\n\n\ndef ana_sayfa(request):\n    sayi = Yazi.objects.filter(yayinda=True).count()\n    html = f"<h1>Blogum</h1><p>Yayında {sayi} yazı var.</p>"\n    return HttpResponse(html)\n', 'blog/urls.py': 'from django.urls import path\n\nfrom . import views\n\nurlpatterns = [\n    path("", views.ana_sayfa, name="ana_sayfa"),\n]\n'}}
AYAR_DEGISIKLIKLERI = [('    "django.contrib.staticfiles",\n]', '    "django.contrib.staticfiles",\n    "blog",\n]'), ('LANGUAGE_CODE = "en-us"', 'LANGUAGE_CODE = "tr"'), ('TIME_ZONE = "UTC"', 'TIME_ZONE = "Europe/Istanbul"')]
EK_AYAR = ''


def calistir(*args, **kw):
    subprocess.run([sys.executable, *args], check=True, **kw)


if Path("manage.py").exists():
    print("manage.py var: mevcut proje kullanılacak.")
else:
    calistir("-m", "django", "startproject", "sitem", ".")
    ayar = Path("sitem/settings.py")
    metin = ayar.read_text(encoding="utf-8")
    for eski, yeni in AYAR_DEGISIKLIKLERI:
        metin = metin.replace(eski, yeni)
    ayar.write_text(metin + EK_AYAR, encoding="utf-8")
    for asama, dosyalar in ASAMALAR.items():
        for ad, icerik in dosyalar.items():
            Path(ad).parent.mkdir(parents=True, exist_ok=True)
            Path(ad).write_text(icerik, encoding="utf-8")
        calistir("manage.py", "makemigrations", "blog")
    calistir("manage.py", "migrate")
    ortam = dict(os.environ, DJANGO_SUPERUSER_USERNAME="admin",
                 DJANGO_SUPERUSER_EMAIL="admin@ornek.com", DJANGO_SUPERUSER_PASSWORD="DersSifre-2026")
    calistir("manage.py", "createsuperuser", "--noinput", env=ortam)
    calistir("manage.py", "shell", "-c",
             "from blog.models import Yazi\n"
             "Yazi.objects.create(baslik='Neden Python öğreniyorum?', icerik='Veri ve web için.', yayinda=True)\n"
             "Yazi.objects.create(baslik='Pandas ile ilk veri temizliğim', icerik='to_numeric çok işe yaradı.', yayinda=True)\n"
             "Yazi.objects.create(baslik='Django\\'da ilk günüm', icerik='Admin paneline bayıldım.', yayinda=True)")
    print("Ders 26 sonundaki proje kuruldu (admin / DersSifre-2026).")


# %% Adım 1 — İlk şablon ve render (views.py, urls.py, yazi_listesi.html — sade sürüm)
from pathlib import Path

dosyalar = {
    "blog/templates/blog/yazi_listesi.html": """<!DOCTYPE html>
<html lang="tr">
<head><meta charset="utf-8"><title>Blogum</title></head>
<body>
  <h1>Son yazılar</h1>
  {% for yazi in yazilar %}
    <h2>{{ yazi.baslik }}</h2>
    <p>{{ yazi.olusturma|date:"j F Y" }}</p>
    <p>{{ yazi.icerik|truncatewords:12 }}</p>
  {% empty %}
    <p>Henüz yayında yazı yok.</p>
  {% endfor %}
</body>
</html>
""",
    "blog/views.py": """from django.shortcuts import render

from .models import Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar})
""",
    "blog/urls.py": """from django.urls import path

from . import views

urlpatterns = [
    path("", views.yazi_listesi, name="yazi_listesi"),
]
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 2 — Filtreleri shell'de denemek
import subprocess
import sys

# Terminaldeki karşılığı: python manage.py shell  →  satırları tek tek yazın
kod = 'from datetime import datetime\nfrom django.template import Context, Template\n\nsablon = Template("""{{ ad|upper }} · {{ ad|length }} harf\n{{ tarih|date:"j F Y, l" }}\n{{ metin|truncatewords:4 }}\n{{ etiketler|join:", " }}\n{{ puan|default:"puan yok" }}\n{{ fiyat|floatformat:2 }} TL""")\nprint(sablon.render(Context({\n    "ad": "Deniz", "tarih": datetime(2026, 10, 27),\n    "metin": "Django şablon dili HTML\'i veriyle doldurur.",\n    "etiketler": ["python", "django", "web"],\n    "puan": None, "fiyat": 1249.5})))'
subprocess.run([sys.executable, "manage.py", "shell", "-c", kod], check=True)


# %% Adım 3 — base.html, Bootstrap'li liste şablonu ve stil.css
from pathlib import Path

dosyalar = {
    "blog/templates/blog/base.html": """{% load static %}
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block baslik %}Blogum{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="{% static 'blog/stil.css' %}" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand bg-dark" data-bs-theme="dark">
  <div class="container">
    <a class="navbar-brand" href="{% url 'yazi_listesi' %}">Blogum</a>
    <div class="navbar-nav">
    </div>
  </div>
</nav>
<main class="container py-4">
  {% block icerik %}{% endblock %}
</main>
<footer class="text-center text-secondary py-3">© 2026 Blogum · Django ile yapıldı</footer>
</body>
</html>
""",
    "blog/templates/blog/yazi_listesi.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <h1 class="mb-4">{% if kategori %}{{ kategori.ad }}{% else %}Son yazılar{% endif %}</h1>
  {% for yazi in yazilar %}
    <article class="card mb-3">
      <div class="card-body">
        <h2 class="h4">{{ yazi.baslik }}</h2>
        <p class="text-secondary small">
          {{ yazi.olusturma|date:"j F Y" }}
        </p>
        <p>{{ yazi.icerik|truncatewords:25 }}</p>
      </div>
    </article>
  {% empty %}
    <p>Henüz yayında yazı yok.</p>
  {% endfor %}
{% endblock %}
""",
    "blog/static/blog/stil.css": """article h2 a { text-decoration: none; }
article h2 a:hover { text-decoration: underline; }
.navbar-brand { font-weight: 700; }
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 4 — Kategori modeli ve ForeignKey (models.py, admin.py)
from pathlib import Path

dosyalar = {
    "blog/models.py": """from django.db import models
from django.urls import reverse


class Kategori(models.Model):
    ad = models.CharField("Ad", max_length=50, unique=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ["ad"]

    def __str__(self):
        return self.ad


class Yazi(models.Model):
    baslik = models.CharField("Başlık", max_length=200)
    icerik = models.TextField("İçerik")
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="yazilar", verbose_name="Kategori")
    olusturma = models.DateTimeField("Oluşturulma", auto_now_add=True)
    yayinda = models.BooleanField("Yayında", default=False)

    class Meta:
        verbose_name = "Yazı"
        verbose_name_plural = "Yazılar"
        ordering = ["-olusturma"]

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse("yazi_detay", args=[self.pk])
""",
    "blog/admin.py": """from django.contrib import admin

from .models import Kategori, Yazi


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ("ad",)


@admin.register(Yazi)
class YaziAdmin(admin.ModelAdmin):
    list_display = ("baslik", "kategori", "yayinda", "olusturma")
    list_filter = ("yayinda", "kategori")
    search_fields = ("baslik", "icerik")
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 4b — makemigrations
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'makemigrations', 'blog'], check=True)


# %% Adım 4c — migrate
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)


# %% Adım 4d — Örnek kategoriler ve atamalar
import subprocess
import sys

# Terminaldeki karşılığı: python manage.py shell  →  satırları tek tek yazın
kod = 'from blog.models import Kategori, Yazi\n\nfor ad in ["Kişisel", "Veri", "Web"]:\n    Kategori.objects.get_or_create(ad=ad)\nfor yazi in Yazi.objects.filter(kategori__isnull=True):\n    if "Pandas" in yazi.baslik or "Matplotlib" in yazi.baslik:\n        yazi.kategori = Kategori.objects.get(ad="Veri")\n    elif "Django" in yazi.baslik:\n        yazi.kategori = Kategori.objects.get(ad="Web")\n    else:\n        yazi.kategori = Kategori.objects.get(ad="Kişisel")\n    yazi.save()\nprint(Kategori.objects.count(), "kategori hazır")'
subprocess.run([sys.executable, "manage.py", "shell", "-c", kod], check=True)


# %% Adım 5 — İlişkili sorgular
import subprocess
import sys

# Terminaldeki karşılığı: python manage.py shell  →  satırları tek tek yazın
kod = 'from blog.models import Kategori, Yazi\n\ny = Yazi.objects.get(baslik__startswith="Pandas")\nprint(y.kategori, "|", y.kategori.ad)\nveri = Kategori.objects.get(ad="Veri")\nbasliklar = [x.baslik for x in veri.yazilar.all()]\nprint(veri.yazilar.count(), "yazı:", basliklar)\nprint(Yazi.objects.filter(kategori__ad="Web", yayinda=True))\nprint(Yazi.objects.filter(kategori__isnull=True).count())'
subprocess.run([sys.executable, "manage.py", "shell", "-c", kod], check=True)


# %% Adım 5b — ORM'nin ürettiği SQL
import subprocess
import sys

# Terminaldeki karşılığı: python manage.py shell  →  satırları tek tek yazın
kod = 'from blog.models import Yazi\n\nsorgu = Yazi.objects.filter(kategori__ad="Web", yayinda=True)\nprint(sorgu.query)'
subprocess.run([sys.executable, "manage.py", "shell", "-c", kod], check=True)


# %% Adım 6 — Detay ve kategori sayfaları, context processor, tam şablonlar
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.shortcuts import get_object_or_404, render

from .models import Kategori, Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar})


def yazi_detay(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)
    return render(request, "blog/yazi_detay.html", {"yazi": yazi})


def kategori(request, pk):
    kat = get_object_or_404(Kategori, pk=pk)
    yazilar = kat.yazilar.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})
""",
    "blog/urls.py": """from django.urls import path

from . import views

urlpatterns = [
    path("", views.yazi_listesi, name="yazi_listesi"),
    path("yazi/<int:pk>/", views.yazi_detay, name="yazi_detay"),
    path("kategori/<int:pk>/", views.kategori, name="kategori"),
]
""",
    "blog/context_processors.py": """from .models import Kategori


def kategoriler(request):
    return {"tum_kategoriler": Kategori.objects.all()}
""",
    "blog/templates/blog/base.html": """{% load static %}
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block baslik %}Blogum{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="{% static 'blog/stil.css' %}" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand bg-dark" data-bs-theme="dark">
  <div class="container">
    <a class="navbar-brand" href="{% url 'yazi_listesi' %}">Blogum</a>
    <div class="navbar-nav">
      {% for k in tum_kategoriler %}
        <a class="nav-link" href="{% url 'kategori' k.pk %}">{{ k.ad }}</a>
      {% endfor %}
    </div>
  </div>
</nav>
<main class="container py-4">
  {% block icerik %}{% endblock %}
</main>
<footer class="text-center text-secondary py-3">© 2026 Blogum · Django ile yapıldı</footer>
</body>
</html>
""",
    "blog/templates/blog/yazi_listesi.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <h1 class="mb-4">{% if kategori %}{{ kategori.ad }}{% else %}Son yazılar{% endif %}</h1>
  {% for yazi in yazilar %}
    <article class="card mb-3">
      <div class="card-body">
        <h2 class="h4"><a href="{{ yazi.get_absolute_url }}">{{ yazi.baslik }}</a></h2>
        <p class="text-secondary small">
          {{ yazi.olusturma|date:"j F Y" }}
          {% if yazi.kategori %}· {{ yazi.kategori.ad }}{% endif %}
        </p>
        <p>{{ yazi.icerik|truncatewords:25 }}</p>
      </div>
    </article>
  {% empty %}
    <p>Henüz yayında yazı yok.</p>
  {% endfor %}
{% endblock %}
""",
    "blog/templates/blog/yazi_detay.html": """{% extends "blog/base.html" %}

{% block baslik %}{{ yazi.baslik }} · Blogum{% endblock %}

{% block icerik %}
  <article>
    <h1>{{ yazi.baslik }}</h1>
    <p class="text-secondary">
      {{ yazi.olusturma|date:"j F Y, H:i" }}
      {% if yazi.kategori %}·
        <a href="{% url 'kategori' yazi.kategori.pk %}">{{ yazi.kategori.ad }}</a>
      {% endif %}
    </p>
    <div class="fs-5">{{ yazi.icerik|linebreaks }}</div>
  </article>
  <a href="{% url 'yazi_listesi' %}" class="btn btn-outline-primary mt-3">← Tüm yazılar</a>
{% endblock %}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 6b — settings.py: context processor ekle
from pathlib import Path

ayar = Path("sitem/settings.py")
metin = ayar.read_text(encoding="utf-8")
eski = '                "django.contrib.messages.context_processors.messages",\n'
yeni = '                "django.contrib.messages.context_processors.messages",\n                "blog.context_processors.kategoriler",\n'
if "blog.context_processors.kategoriler" not in metin:
    metin = metin.replace(eski, yeni)
    ayar.write_text(metin, encoding="utf-8")
print("context processor:", "blog.context_processors.kategoriler" in metin)


# %% Alıştırma 1 — çözüm (hakkimda)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.shortcuts import get_object_or_404, render

from .models import Kategori, Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar})


def yazi_detay(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)
    return render(request, "blog/yazi_detay.html", {"yazi": yazi})


def kategori(request, pk):
    kat = get_object_or_404(Kategori, pk=pk)
    yazilar = kat.yazilar.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})


def hakkimda(request):
    return render(request, "blog/hakkimda.html")
""",
    "blog/urls.py": """from django.urls import path

from . import views

urlpatterns = [
    path("", views.yazi_listesi, name="yazi_listesi"),
    path("yazi/<int:pk>/", views.yazi_detay, name="yazi_detay"),
    path("kategori/<int:pk>/", views.kategori, name="kategori"),
    path("hakkimda/", views.hakkimda, name="hakkimda"),
]
""",
    "blog/templates/blog/base.html": """{% load static %}
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block baslik %}Blogum{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="{% static 'blog/stil.css' %}" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand bg-dark" data-bs-theme="dark">
  <div class="container">
    <a class="navbar-brand" href="{% url 'yazi_listesi' %}">Blogum</a>
    <div class="navbar-nav">
      {% for k in tum_kategoriler %}
        <a class="nav-link" href="{% url 'kategori' k.pk %}">{{ k.ad }}</a>
      {% endfor %}
      <a class="nav-link" href="{% url 'hakkimda' %}">Hakkımda</a>
    </div>
  </div>
</nav>
<main class="container py-4">
  {% block icerik %}{% endblock %}
</main>
<footer class="text-center text-secondary py-3">© 2026 Blogum · Django ile yapıldı</footer>
</body>
</html>
""",
    "blog/templates/blog/hakkimda.html": """{% extends "blog/base.html" %}

{% block baslik %}Hakkımda · Blogum{% endblock %}

{% block icerik %}
  <h1>Hakkımda</h1>
  <p class="lead">Merhaba, ben Deniz. Python ve web öğreniyorum.</p>
  <p>Bu blogda öğrendiklerimi ve projelerimi paylaşıyorum.</p>
  <a href="{% url 'yazi_listesi' %}" class="btn btn-primary">Yazılarımı oku</a>
{% endblock %}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 2 — çözüm (arama)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Kategori, Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    q = request.GET.get("q", "").strip()
    if q:
        yazilar = yazilar.filter(Q(baslik__icontains=q) | Q(icerik__icontains=q))
    return render(request, "blog/yazi_listesi.html",
                  {"yazilar": yazilar, "q": q})


def yazi_detay(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)
    return render(request, "blog/yazi_detay.html", {"yazi": yazi})


def kategori(request, pk):
    kat = get_object_or_404(Kategori, pk=pk)
    yazilar = kat.yazilar.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})


def hakkimda(request):
    return render(request, "blog/hakkimda.html")
""",
    "blog/templates/blog/base.html": """{% load static %}
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block baslik %}Blogum{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="{% static 'blog/stil.css' %}" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand bg-dark" data-bs-theme="dark">
  <div class="container">
    <a class="navbar-brand" href="{% url 'yazi_listesi' %}">Blogum</a>
    <div class="navbar-nav">
      {% for k in tum_kategoriler %}
        <a class="nav-link" href="{% url 'kategori' k.pk %}">{{ k.ad }}</a>
      {% endfor %}
      <a class="nav-link" href="{% url 'hakkimda' %}">Hakkımda</a>
    </div>
    <form class="d-flex ms-auto" action="{% url 'yazi_listesi' %}">
      <input class="form-control me-2" name="q"
             placeholder="Ara…" value="{{ q }}">
      <button class="btn btn-outline-light">Ara</button>
    </form>
  </div>
</nav>
<main class="container py-4">
  {% block icerik %}{% endblock %}
</main>
<footer class="text-center text-secondary py-3">© 2026 Blogum · Django ile yapıldı</footer>
</body>
</html>
""",
    "blog/templates/blog/yazi_listesi.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <h1 class="mb-4">{% if kategori %}{{ kategori.ad }}{% elif q %}“{{ q }}” için sonuçlar{% else %}Son yazılar{% endif %}</h1>
  {% for yazi in yazilar %}
    <article class="card mb-3">
      <div class="card-body">
        <h2 class="h4"><a href="{{ yazi.get_absolute_url }}">{{ yazi.baslik }}</a></h2>
        <p class="text-secondary small">
          {{ yazi.olusturma|date:"j F Y" }}
          {% if yazi.kategori %}· {{ yazi.kategori.ad }}{% endif %}
        </p>
        <p>{{ yazi.icerik|truncatewords:25 }}</p>
      </div>
    </article>
  {% empty %}
    <p>Henüz yayında yazı yok.</p>
  {% endfor %}
{% endblock %}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 3 — çözüm (sayfalama)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Kategori, Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    q = request.GET.get("q", "").strip()
    if q:
        yazilar = yazilar.filter(Q(baslik__icontains=q) | Q(icerik__icontains=q))
    sayfa = Paginator(yazilar, 2).get_page(request.GET.get("sayfa"))
    return render(request, "blog/yazi_listesi.html", {"yazilar": sayfa, "sayfa": sayfa, "q": q})


def yazi_detay(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)
    return render(request, "blog/yazi_detay.html", {"yazi": yazi})


def kategori(request, pk):
    kat = get_object_or_404(Kategori, pk=pk)
    yazilar = kat.yazilar.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})


def hakkimda(request):
    return render(request, "blog/hakkimda.html")
""",
    "blog/templates/blog/yazi_listesi.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <h1 class="mb-4">{% if kategori %}{{ kategori.ad }}{% elif q %}“{{ q }}” için sonuçlar{% else %}Son yazılar{% endif %}</h1>
  {% for yazi in yazilar %}
    <article class="card mb-3">
      <div class="card-body">
        <h2 class="h4"><a href="{{ yazi.get_absolute_url }}">{{ yazi.baslik }}</a></h2>
        <p class="text-secondary small">
          {{ yazi.olusturma|date:"j F Y" }}
          {% if yazi.kategori %}· {{ yazi.kategori.ad }}{% endif %}
        </p>
        <p>{{ yazi.icerik|truncatewords:25 }}</p>
      </div>
    </article>
  {% empty %}
    <p>Henüz yayında yazı yok.</p>
  {% endfor %}
  {% if sayfa %}
    <nav class="mt-3">
      {% if sayfa.has_previous %}
        <a class="btn btn-outline-secondary"
           href="?sayfa={{ sayfa.previous_page_number }}&q={{ q|urlencode }}">
          ← Önceki</a>
      {% endif %}
      <span class="mx-2">Sayfa {{ sayfa.number }} /
        {{ sayfa.paginator.num_pages }}</span>
      {% if sayfa.has_next %}
        <a class="btn btn-outline-secondary"
           href="?sayfa={{ sayfa.next_page_number }}&q={{ q|urlencode }}">
          Sonraki →</a>
      {% endif %}
    </nav>
  {% endif %}
{% endblock %}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")
