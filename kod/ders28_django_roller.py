# =============================================================================
# Python Kursu — Ders 28 (Hafta 14, Gün 2)
# Konu: GET ve POST, Yorum modeli, ModelForm, doğrulama, CSRF, mesajlar, admin inline ve eylemler, kimlik doğrulama (giriş/çıkış), User/Group/Permission, login_required, permission_required, sahiplik kontrolü, şablonda user ve perms, yayınlama kontrol listesi — yorumlu ve yazar rollü blog
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Ders 27'deki blog_projesi klasöründe, sanal ortam etkinken çalışın (ya da blog_ders27.zip'i açın). Proje yoksa Bölüm 0 kurar.
#   - Hücreler model, form, view, URL ve şablon dosyalarını yazar; makemigrations/migrate çalıştırır; 'Yazarlar' grubunu ve 'ayse' kullanıcısını oluşturur.
#   - Örnek hesaplar: admin / DersSifre-2026 (yönetici), ayse / DersSifre-2026 (Yazarlar grubu). Kendi projenizde güçlü, size özel şifreler kullanın.
#   - Sunucu: python manage.py runserver → http://127.0.0.1:8000  ·  giriş: /hesap/login/
# =============================================================================


# %% Bölüm 0 — Ders 27 projesi yoksa kur (bir kez)
import os
import subprocess
import sys
from pathlib import Path

# Önceki dersin projesi bu klasörde yoksa onu sıfırdan kurar (varsa hiçbir şey yapmaz).
ASAMALAR = {26: {'sitem/urls.py': 'from django.contrib import admin\nfrom django.urls import include, path\n\nurlpatterns = [\n    path("admin/", admin.site.urls),\n    path("", include("blog.urls")),\n]\n', 'blog/__init__.py': '', 'blog/apps.py': 'from django.apps import AppConfig\n\n\nclass BlogConfig(AppConfig):\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "blog"\n    verbose_name = "Blog"\n', 'blog/models.py': 'from django.db import models\n\n\nclass Yazi(models.Model):\n    baslik = models.CharField("Başlık", max_length=200)\n    icerik = models.TextField("İçerik")\n    olusturma = models.DateTimeField("Oluşturulma", auto_now_add=True)\n    yayinda = models.BooleanField("Yayında", default=False)\n\n    class Meta:\n        verbose_name = "Yazı"\n        verbose_name_plural = "Yazılar"\n        ordering = ["-olusturma"]\n\n    def __str__(self):\n        return self.baslik\n', 'blog/admin.py': 'from django.contrib import admin\n\nfrom .models import Yazi\n\n\n@admin.register(Yazi)\nclass YaziAdmin(admin.ModelAdmin):\n    list_display = ("baslik", "yayinda", "olusturma")\n    list_filter = ("yayinda",)\n    search_fields = ("baslik", "icerik")\n', 'blog/views.py': 'from django.http import HttpResponse\n\nfrom .models import Yazi\n\n\ndef ana_sayfa(request):\n    sayi = Yazi.objects.filter(yayinda=True).count()\n    html = f"<h1>Blogum</h1><p>Yayında {sayi} yazı var.</p>"\n    return HttpResponse(html)\n', 'blog/urls.py': 'from django.urls import path\n\nfrom . import views\n\nurlpatterns = [\n    path("", views.ana_sayfa, name="ana_sayfa"),\n]\n'}, 27: {'sitem/urls.py': 'from django.contrib import admin\nfrom django.urls import include, path\n\nurlpatterns = [\n    path("admin/", admin.site.urls),\n    path("", include("blog.urls")),\n]\n', 'blog/__init__.py': '', 'blog/apps.py': 'from django.apps import AppConfig\n\n\nclass BlogConfig(AppConfig):\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "blog"\n    verbose_name = "Blog"\n', 'blog/models.py': 'from django.db import models\nfrom django.urls import reverse\n\n\nclass Kategori(models.Model):\n    ad = models.CharField("Ad", max_length=50, unique=True)\n\n    class Meta:\n        verbose_name = "Kategori"\n        verbose_name_plural = "Kategoriler"\n        ordering = ["ad"]\n\n    def __str__(self):\n        return self.ad\n\n\nclass Yazi(models.Model):\n    baslik = models.CharField("Başlık", max_length=200)\n    icerik = models.TextField("İçerik")\n    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True,\n                                 related_name="yazilar", verbose_name="Kategori")\n    olusturma = models.DateTimeField("Oluşturulma", auto_now_add=True)\n    yayinda = models.BooleanField("Yayında", default=False)\n\n    class Meta:\n        verbose_name = "Yazı"\n        verbose_name_plural = "Yazılar"\n        ordering = ["-olusturma"]\n\n    def __str__(self):\n        return self.baslik\n\n    def get_absolute_url(self):\n        return reverse("yazi_detay", args=[self.pk])\n', 'blog/admin.py': 'from django.contrib import admin\n\nfrom .models import Kategori, Yazi\n\n\n@admin.register(Kategori)\nclass KategoriAdmin(admin.ModelAdmin):\n    list_display = ("ad",)\n\n\n@admin.register(Yazi)\nclass YaziAdmin(admin.ModelAdmin):\n    list_display = ("baslik", "kategori", "yayinda", "olusturma")\n    list_filter = ("yayinda", "kategori")\n    search_fields = ("baslik", "icerik")\n', 'blog/views.py': 'from django.shortcuts import get_object_or_404, render\n\nfrom .models import Kategori, Yazi\n\n\ndef yazi_listesi(request):\n    yazilar = Yazi.objects.filter(yayinda=True)\n    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar})\n\n\ndef yazi_detay(request, pk):\n    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)\n    return render(request, "blog/yazi_detay.html", {"yazi": yazi})\n\n\ndef kategori(request, pk):\n    kat = get_object_or_404(Kategori, pk=pk)\n    yazilar = kat.yazilar.filter(yayinda=True)\n    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})\n', 'blog/urls.py': 'from django.urls import path\n\nfrom . import views\n\nurlpatterns = [\n    path("", views.yazi_listesi, name="yazi_listesi"),\n    path("yazi/<int:pk>/", views.yazi_detay, name="yazi_detay"),\n    path("kategori/<int:pk>/", views.kategori, name="kategori"),\n]\n', 'blog/context_processors.py': 'from .models import Kategori\n\n\ndef kategoriler(request):\n    return {"tum_kategoriler": Kategori.objects.all()}\n', 'blog/templates/blog/base.html': '{% load static %}\n<!DOCTYPE html>\n<html lang="tr">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <title>{% block baslik %}Blogum{% endblock %}</title>\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">\n  <link href="{% static \'blog/stil.css\' %}" rel="stylesheet">\n</head>\n<body>\n<nav class="navbar navbar-expand bg-dark" data-bs-theme="dark">\n  <div class="container">\n    <a class="navbar-brand" href="{% url \'yazi_listesi\' %}">Blogum</a>\n    <div class="navbar-nav">\n      {% for k in tum_kategoriler %}\n        <a class="nav-link" href="{% url \'kategori\' k.pk %}">{{ k.ad }}</a>\n      {% endfor %}\n    </div>\n  </div>\n</nav>\n<main class="container py-4">\n  {% block icerik %}{% endblock %}\n</main>\n<footer class="text-center text-secondary py-3">© 2026 Blogum · Django ile yapıldı</footer>\n</body>\n</html>\n', 'blog/templates/blog/yazi_listesi.html': '{% extends "blog/base.html" %}\n\n{% block icerik %}\n  <h1 class="mb-4">{% if kategori %}{{ kategori.ad }}{% else %}Son yazılar{% endif %}</h1>\n  {% for yazi in yazilar %}\n    <article class="card mb-3">\n      <div class="card-body">\n        <h2 class="h4"><a href="{{ yazi.get_absolute_url }}">{{ yazi.baslik }}</a></h2>\n        <p class="text-secondary small">\n          {{ yazi.olusturma|date:"j F Y" }}\n          {% if yazi.kategori %}· {{ yazi.kategori.ad }}{% endif %}\n        </p>\n        <p>{{ yazi.icerik|truncatewords:25 }}</p>\n      </div>\n    </article>\n  {% empty %}\n    <p>Henüz yayında yazı yok.</p>\n  {% endfor %}\n{% endblock %}\n', 'blog/templates/blog/yazi_detay.html': '{% extends "blog/base.html" %}\n\n{% block baslik %}{{ yazi.baslik }} · Blogum{% endblock %}\n\n{% block icerik %}\n  <article>\n    <h1>{{ yazi.baslik }}</h1>\n    <p class="text-secondary">\n      {{ yazi.olusturma|date:"j F Y, H:i" }}\n      {% if yazi.kategori %}·\n        <a href="{% url \'kategori\' yazi.kategori.pk %}">{{ yazi.kategori.ad }}</a>\n      {% endif %}\n    </p>\n    <div class="fs-5">{{ yazi.icerik|linebreaks }}</div>\n  </article>\n  <a href="{% url \'yazi_listesi\' %}" class="btn btn-outline-primary mt-3">← Tüm yazılar</a>\n{% endblock %}\n', 'blog/static/blog/stil.css': 'article h2 a { text-decoration: none; }\narticle h2 a:hover { text-decoration: underline; }\n.navbar-brand { font-weight: 700; }\n'}}
AYAR_DEGISIKLIKLERI = [('    "django.contrib.staticfiles",\n]', '    "django.contrib.staticfiles",\n    "blog",\n]'), ('LANGUAGE_CODE = "en-us"', 'LANGUAGE_CODE = "tr"'), ('TIME_ZONE = "UTC"', 'TIME_ZONE = "Europe/Istanbul"'), ('                "django.contrib.messages.context_processors.messages",\n', '                "django.contrib.messages.context_processors.messages",\n                "blog.context_processors.kategoriler",\n')]
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
    print("Ders 27 sonundaki proje kuruldu (admin / DersSifre-2026).")


# %% Adım 1 — Yorum modeli (models.py) ve admin
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


class Yorum(models.Model):
    yazi = models.ForeignKey(Yazi, on_delete=models.CASCADE,
                             related_name="yorumlar")
    ad = models.CharField("Adınız", max_length=80)
    metin = models.TextField("Yorumunuz", max_length=1000)
    tarih = models.DateTimeField(auto_now_add=True)
    onayli = models.BooleanField("Onaylı", default=False)

    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        ordering = ["tarih"]

    def __str__(self):
        return f"{self.ad}: {self.metin[:30]}"
""",
    "blog/admin.py": """from django.contrib import admin

from .models import Kategori, Yazi, Yorum


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ("ad",)


class YorumInline(admin.TabularInline):
    model = Yorum
    extra = 0


@admin.register(Yazi)
class YaziAdmin(admin.ModelAdmin):
    list_display = ("baslik", "kategori", "yayinda", "olusturma")
    list_filter = ("yayinda", "kategori")
    search_fields = ("baslik", "icerik")
    list_editable = ("yayinda",)
    inlines = [YorumInline]


@admin.register(Yorum)
class YorumAdmin(admin.ModelAdmin):
    list_display = ("ad", "yazi", "tarih", "onayli")
    list_filter = ("onayli",)
    actions = ["onayla"]

    @admin.action(description="Seçili yorumları onayla")
    def onayla(self, request, queryset):
        sayi = queryset.update(onayli=True)
        self.message_user(request, f"{sayi} yorum onaylandı.")
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 1b — makemigrations
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'makemigrations', 'blog'], check=True)


# %% Adım 1c — migrate
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)


# %% Adım 2 — forms.py
from pathlib import Path

dosyalar = {
    "blog/forms.py": """from django import forms

from .models import Yazi, Yorum


class BootstrapForm(forms.ModelForm):
    \"\"\"Bütün alanlara Bootstrap sınıfı ekler.\"\"\"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for alan in self.fields.values():
            if isinstance(alan.widget, forms.CheckboxInput):
                alan.widget.attrs["class"] = "form-check-input"
            else:
                alan.widget.attrs["class"] = "form-control"


class YorumForm(BootstrapForm):
    class Meta:
        model = Yorum
        fields = ["ad", "metin"]
        widgets = {"metin": forms.Textarea(attrs={"rows": 3})}


class YaziForm(BootstrapForm):
    class Meta:
        model = Yazi
        fields = ["baslik", "kategori", "icerik", "yayinda"]
        widgets = {"icerik": forms.Textarea(attrs={"rows": 8})}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 3 — Detay view'u (POST) ve şablonlar (mesajlar dahil)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import YorumForm
from .models import Kategori, Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar})


def yazi_detay(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)
    if request.method == "POST":
        form = YorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.yazi = yazi
            yorum.save()
            messages.success(request, "Teşekkürler! Yorumunuz onaydan sonra görünecek.")
            return redirect(yazi)
    else:
        form = YorumForm()
    yorumlar = yazi.yorumlar.filter(onayli=True)
    return render(request, "blog/yazi_detay.html",
                  {"yazi": yazi, "yorumlar": yorumlar, "form": form})


def kategori(request, pk):
    kat = get_object_or_404(Kategori, pk=pk)
    yazilar = kat.yazilar.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})
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
  <section class="mt-5">
    <h2 class="h4">Yorumlar ({{ yorumlar|length }})</h2>
    {% for y in yorumlar %}
      <div class="border-start border-3 ps-3 mb-3">
        <b>{{ y.ad }}</b> <span class="text-secondary small">{{ y.tarih|date:"j F Y" }}</span>
        <p class="mb-0">{{ y.metin }}</p>
      </div>
    {% empty %}
      <p class="text-secondary">İlk yorumu siz yazın.</p>
    {% endfor %}
    <form method="post" class="mt-3" style="max-width: 560px">
      {% csrf_token %}
      {{ form.as_p }}
      <button class="btn btn-primary">Gönder</button>
    </form>
  </section>
  <a href="{% url 'yazi_listesi' %}" class="btn btn-outline-primary mt-3">← Tüm yazılar</a>
{% endblock %}
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
  {% for m in messages %}
    <div class="alert alert-success">{{ m }}</div>
  {% endfor %}
  {% block icerik %}{% endblock %}
</main>
<footer class="text-center text-secondary py-3">© 2026 Blogum · Django ile yapıldı</footer>
</body>
</html>
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 4 — Admin: inline ve toplu onay eylemi
from pathlib import Path

dosyalar = {
    "blog/admin.py": """from django.contrib import admin

from .models import Kategori, Yazi, Yorum


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ("ad",)


class YorumInline(admin.TabularInline):
    model = Yorum
    extra = 0


@admin.register(Yazi)
class YaziAdmin(admin.ModelAdmin):
    list_display = ("baslik", "kategori", "yayinda", "olusturma")
    list_filter = ("yayinda", "kategori")
    search_fields = ("baslik", "icerik")
    list_editable = ("yayinda",)
    inlines = [YorumInline]


@admin.register(Yorum)
class YorumAdmin(admin.ModelAdmin):
    list_display = ("ad", "yazi", "tarih", "onayli")
    list_filter = ("onayli",)
    actions = ["onayla"]

    @admin.action(description="Seçili yorumları onayla")
    def onayla(self, request, queryset):
        sayi = queryset.update(onayli=True)
        self.message_user(request, f"{sayi} yorum onaylandı.")
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 5 — Giriş/çıkış: URL'ler, ayarlar, login şablonu
from pathlib import Path

dosyalar = {
    "sitem/urls.py": """from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hesap/", include("django.contrib.auth.urls")),
    path("", include("blog.urls")),
]
""",
    "blog/templates/registration/login.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <h1>Giriş</h1>
  <form method="post" style="max-width: 400px">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-primary">Giriş yap</button>
  </form>
{% endblock %}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 5b — settings.py: giriş/çıkış yönlendirmeleri
from pathlib import Path

ayar = Path("sitem/settings.py")
metin = ayar.read_text(encoding="utf-8")
if "LOGIN_REDIRECT_URL" not in metin:
    metin += '\nLOGIN_URL = "login"\nLOGIN_REDIRECT_URL = "panel"\nLOGOUT_REDIRECT_URL = "yazi_listesi"\n'
    ayar.write_text(metin, encoding="utf-8")
print("giriş ayarları:", "LOGIN_REDIRECT_URL" in metin)


# %% Adım 6 — Yazar alanı (models.py)
from pathlib import Path

dosyalar = {
    "blog/models.py": """from django.conf import settings
from django.db import models
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
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              null=True, related_name="yazilar", verbose_name="Yazar")
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


class Yorum(models.Model):
    yazi = models.ForeignKey(Yazi, on_delete=models.CASCADE,
                             related_name="yorumlar")
    ad = models.CharField("Adınız", max_length=80)
    metin = models.TextField("Yorumunuz", max_length=1000)
    tarih = models.DateTimeField(auto_now_add=True)
    onayli = models.BooleanField("Onaylı", default=False)

    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        ordering = ["tarih"]

    def __str__(self):
        return f"{self.ad}: {self.metin[:30]}"
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 6b — makemigrations
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'makemigrations', 'blog'], check=True)


# %% Adım 6c — migrate
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)


# %% Adım 7 — 'Yazarlar' grubu ve 'ayse' kullanıcısı
import subprocess
import sys

# Terminaldeki karşılığı: python manage.py shell  →  satırları tek tek yazın
kod = 'from django.contrib.auth.models import Group, Permission, User\n\nyazarlar, _ = Group.objects.get_or_create(name="Yazarlar")\nizinler = Permission.objects.filter(\n    codename__in=["add_yazi", "view_yazi"])\nyazarlar.permissions.set(izinler)\nprint([p.codename for p in yazarlar.permissions.all()])\nayse, yeni = User.objects.get_or_create(username="ayse")\nif yeni:\n    ayse.set_password("DersSifre-2026")\n    ayse.save()\nayse.groups.add(yazarlar)\nprint(ayse.has_perm("blog.add_yazi"))\nprint(ayse.has_perm("blog.delete_yazi"))'
subprocess.run([sys.executable, "manage.py", "shell", "-c", kod], check=True)


# %% Adım 8 — Formlar, view'lar, URL'ler ve şablonlar (panel, yazı ekle/düzenle)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import YaziForm, YorumForm
from .models import Kategori, Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar})


def kategori(request, pk):
    kat = get_object_or_404(Kategori, pk=pk)
    yazilar = kat.yazilar.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})


def yazi_detay(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)
    if request.method == "POST":
        form = YorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.yazi = yazi
            yorum.save()
            messages.success(request, "Teşekkürler! Yorumunuz onaydan sonra görünecek.")
            return redirect(yazi)
    else:
        form = YorumForm()
    yorumlar = yazi.yorumlar.filter(onayli=True)
    return render(request, "blog/yazi_detay.html",
                  {"yazi": yazi, "yorumlar": yorumlar, "form": form})


@login_required
@permission_required("blog.add_yazi", raise_exception=True)
def yazi_ekle(request):
    form = YaziForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        yazi = form.save(commit=False)
        yazi.yazar = request.user
        yazi.save()
        messages.success(request, "Yazı kaydedildi.")
        return redirect("panel")
    return render(request, "blog/yazi_form.html", {"form": form, "baslik": "Yeni yazı"})


@login_required
def yazi_duzenle(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk)
    if yazi.yazar != request.user and not request.user.has_perm("blog.change_yazi"):
        raise PermissionDenied
    form = YaziForm(request.POST or None, instance=yazi)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Yazı güncellendi.")
        return redirect("panel")
    return render(request, "blog/yazi_form.html", {"form": form, "baslik": "Yazıyı düzenle"})


@login_required
def panel(request):
    yazilar = Yazi.objects.filter(yazar=request.user)
    return render(request, "blog/panel.html", {"yazilar": yazilar})
""",
    "blog/urls.py": """from django.urls import path

from . import views

urlpatterns = [
    path("", views.yazi_listesi, name="yazi_listesi"),
    path("yazi/<int:pk>/", views.yazi_detay, name="yazi_detay"),
    path("kategori/<int:pk>/", views.kategori, name="kategori"),
    path("panel/", views.panel, name="panel"),
    path("yazi/yeni/", views.yazi_ekle, name="yazi_ekle"),
    path("yazi/<int:pk>/duzenle/", views.yazi_duzenle, name="yazi_duzenle"),
]
""",
    "blog/admin.py": """from django.contrib import admin

from .models import Kategori, Yazi, Yorum


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ("ad",)


class YorumInline(admin.TabularInline):
    model = Yorum
    extra = 0


@admin.register(Yazi)
class YaziAdmin(admin.ModelAdmin):
    list_display = ("baslik", "yazar", "kategori", "yayinda", "olusturma")
    list_filter = ("yayinda", "kategori", "yazar")
    search_fields = ("baslik", "icerik")
    list_editable = ("yayinda",)
    inlines = [YorumInline]


@admin.register(Yorum)
class YorumAdmin(admin.ModelAdmin):
    list_display = ("ad", "yazi", "tarih", "onayli")
    list_filter = ("onayli",)
    actions = ["onayla"]

    @admin.action(description="Seçili yorumları onayla")
    def onayla(self, request, queryset):
        sayi = queryset.update(onayli=True)
        self.message_user(request, f"{sayi} yorum onaylandı.")
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
    <div class="navbar-nav ms-auto">
      {% if user.is_authenticated %}
        <a class="nav-link" href="{% url 'panel' %}">Panelim ({{ user.username }})</a>
        <form method="post" action="{% url 'logout' %}">
          {% csrf_token %}
          <button class="btn btn-link nav-link">Çıkış</button>
        </form>
      {% else %}
        <a class="nav-link" href="{% url 'login' %}">Giriş</a>
      {% endif %}
    </div>
  </div>
</nav>
<main class="container py-4">
  {% for m in messages %}
    <div class="alert alert-success">{{ m }}</div>
  {% endfor %}
  {% block icerik %}{% endblock %}
</main>
<footer class="text-center text-secondary py-3">© 2026 Blogum · Django ile yapıldı</footer>
</body>
</html>
""",
    "blog/templates/blog/panel.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Yazılarım</h1>
    {% if perms.blog.add_yazi %}
      <a href="{% url 'yazi_ekle' %}" class="btn btn-success">+ Yeni yazı</a>
    {% endif %}
  </div>
  <table class="table">
    <tr><th>Başlık</th><th>Durum</th><th></th></tr>
    {% for y in yazilar %}
      <tr>
        <td>{{ y.baslik }}</td>
        <td>{% if y.yayinda %}Yayında{% else %}Taslak{% endif %}</td>
        <td><a href="{% url 'yazi_duzenle' y.pk %}">Düzenle</a></td>
      </tr>
    {% empty %}
      <tr><td colspan="3">Henüz yazınız yok.</td></tr>
    {% endfor %}
  </table>
{% endblock %}
""",
    "blog/templates/blog/yazi_form.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <h1>{{ baslik }}</h1>
  <form method="post" style="max-width: 720px">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-primary">Kaydet</button>
    <a href="{% url 'panel' %}" class="btn btn-link">Vazgeç</a>
  </form>
{% endblock %}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 1 — çözüm (onaylı yorum sayısı)
from pathlib import Path

dosyalar = {
    "blog/models.py": """from django.conf import settings
from django.db import models
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
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              null=True, related_name="yazilar", verbose_name="Yazar")
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

    def onayli_yorumlar(self):
        return self.yorumlar.filter(onayli=True)


class Yorum(models.Model):
    yazi = models.ForeignKey(Yazi, on_delete=models.CASCADE,
                             related_name="yorumlar")
    ad = models.CharField("Adınız", max_length=80)
    metin = models.TextField("Yorumunuz", max_length=1000)
    tarih = models.DateTimeField(auto_now_add=True)
    onayli = models.BooleanField("Onaylı", default=False)

    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        ordering = ["tarih"]

    def __str__(self):
        return f"{self.ad}: {self.metin[:30]}"
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
          · {{ yazi.onayli_yorumlar.count }} yorum
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


# %% Alıştırma 2 — çözüm (kayıt ol)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import YaziForm, YorumForm
from .models import Kategori, Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar})


def kategori(request, pk):
    kat = get_object_or_404(Kategori, pk=pk)
    yazilar = kat.yazilar.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})


def yazi_detay(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)
    if request.method == "POST":
        form = YorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.yazi = yazi
            yorum.save()
            messages.success(request, "Teşekkürler! Yorumunuz onaydan sonra görünecek.")
            return redirect(yazi)
    else:
        form = YorumForm()
    yorumlar = yazi.yorumlar.filter(onayli=True)
    return render(request, "blog/yazi_detay.html",
                  {"yazi": yazi, "yorumlar": yorumlar, "form": form})


@login_required
@permission_required("blog.add_yazi", raise_exception=True)
def yazi_ekle(request):
    form = YaziForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        yazi = form.save(commit=False)
        yazi.yazar = request.user
        yazi.save()
        messages.success(request, "Yazı kaydedildi.")
        return redirect("panel")
    return render(request, "blog/yazi_form.html", {"form": form, "baslik": "Yeni yazı"})


@login_required
def yazi_duzenle(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk)
    if yazi.yazar != request.user and not request.user.has_perm("blog.change_yazi"):
        raise PermissionDenied
    form = YaziForm(request.POST or None, instance=yazi)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Yazı güncellendi.")
        return redirect("panel")
    return render(request, "blog/yazi_form.html", {"form": form, "baslik": "Yazıyı düzenle"})


@login_required
def panel(request):
    yazilar = Yazi.objects.filter(yazar=request.user)
    return render(request, "blog/panel.html", {"yazilar": yazilar})


def kayit(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        kullanici = form.save()
        login(request, kullanici)
        messages.success(request, "Hesabınız oluşturuldu.")
        return redirect("yazi_listesi")
    return render(request, "registration/kayit.html", {"form": form})
""",
    "blog/urls.py": """from django.urls import path

from . import views

urlpatterns = [
    path("", views.yazi_listesi, name="yazi_listesi"),
    path("yazi/<int:pk>/", views.yazi_detay, name="yazi_detay"),
    path("kategori/<int:pk>/", views.kategori, name="kategori"),
    path("panel/", views.panel, name="panel"),
    path("yazi/yeni/", views.yazi_ekle, name="yazi_ekle"),
    path("yazi/<int:pk>/duzenle/", views.yazi_duzenle, name="yazi_duzenle"),
    path("hesap/kayit/", views.kayit, name="kayit"),
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
    </div>
    <div class="navbar-nav ms-auto">
      {% if user.is_authenticated %}
        <a class="nav-link" href="{% url 'panel' %}">Panelim ({{ user.username }})</a>
        <form method="post" action="{% url 'logout' %}">
          {% csrf_token %}
          <button class="btn btn-link nav-link">Çıkış</button>
        </form>
      {% else %}
        <a class="nav-link" href="{% url 'login' %}">Giriş</a>
        <a class="nav-link" href="{% url 'kayit' %}">Kayıt ol</a>
      {% endif %}
    </div>
  </div>
</nav>
<main class="container py-4">
  {% for m in messages %}
    <div class="alert alert-success">{{ m }}</div>
  {% endfor %}
  {% block icerik %}{% endblock %}
</main>
<footer class="text-center text-secondary py-3">© 2026 Blogum · Django ile yapıldı</footer>
</body>
</html>
""",
    "blog/templates/registration/kayit.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <h1>Kayıt ol</h1>
  <form method="post" style="max-width: 480px">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-primary">Hesap oluştur</button>
  </form>
{% endblock %}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 3 — çözüm (yazı silme)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import YaziForm, YorumForm
from .models import Kategori, Yazi


def yazi_listesi(request):
    yazilar = Yazi.objects.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar})


def kategori(request, pk):
    kat = get_object_or_404(Kategori, pk=pk)
    yazilar = kat.yazilar.filter(yayinda=True)
    return render(request, "blog/yazi_listesi.html", {"yazilar": yazilar, "kategori": kat})


def yazi_detay(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk, yayinda=True)
    if request.method == "POST":
        form = YorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.yazi = yazi
            yorum.save()
            messages.success(request, "Teşekkürler! Yorumunuz onaydan sonra görünecek.")
            return redirect(yazi)
    else:
        form = YorumForm()
    yorumlar = yazi.yorumlar.filter(onayli=True)
    return render(request, "blog/yazi_detay.html",
                  {"yazi": yazi, "yorumlar": yorumlar, "form": form})


@login_required
@permission_required("blog.add_yazi", raise_exception=True)
def yazi_ekle(request):
    form = YaziForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        yazi = form.save(commit=False)
        yazi.yazar = request.user
        yazi.save()
        messages.success(request, "Yazı kaydedildi.")
        return redirect("panel")
    return render(request, "blog/yazi_form.html", {"form": form, "baslik": "Yeni yazı"})


@login_required
def yazi_duzenle(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk)
    if yazi.yazar != request.user and not request.user.has_perm("blog.change_yazi"):
        raise PermissionDenied
    form = YaziForm(request.POST or None, instance=yazi)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Yazı güncellendi.")
        return redirect("panel")
    return render(request, "blog/yazi_form.html", {"form": form, "baslik": "Yazıyı düzenle"})


@login_required
def panel(request):
    yazilar = Yazi.objects.filter(yazar=request.user)
    return render(request, "blog/panel.html", {"yazilar": yazilar})


def kayit(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        kullanici = form.save()
        login(request, kullanici)
        messages.success(request, "Hesabınız oluşturuldu.")
        return redirect("yazi_listesi")
    return render(request, "registration/kayit.html", {"form": form})


@login_required
def yazi_sil(request, pk):
    yazi = get_object_or_404(Yazi, pk=pk)
    if yazi.yazar != request.user and not request.user.has_perm("blog.delete_yazi"):
        raise PermissionDenied
    if request.method == "POST":
        yazi.delete()
        messages.success(request, "Yazı silindi.")
        return redirect("panel")
    return render(request, "blog/yazi_sil.html", {"yazi": yazi})
""",
    "blog/urls.py": """from django.urls import path

from . import views

urlpatterns = [
    path("", views.yazi_listesi, name="yazi_listesi"),
    path("yazi/<int:pk>/", views.yazi_detay, name="yazi_detay"),
    path("kategori/<int:pk>/", views.kategori, name="kategori"),
    path("panel/", views.panel, name="panel"),
    path("yazi/yeni/", views.yazi_ekle, name="yazi_ekle"),
    path("yazi/<int:pk>/duzenle/", views.yazi_duzenle, name="yazi_duzenle"),
    path("hesap/kayit/", views.kayit, name="kayit"),
    path("yazi/<int:pk>/sil/", views.yazi_sil, name="yazi_sil"),
]
""",
    "blog/templates/blog/panel.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Yazılarım</h1>
    {% if perms.blog.add_yazi %}
      <a href="{% url 'yazi_ekle' %}" class="btn btn-success">+ Yeni yazı</a>
    {% endif %}
  </div>
  <table class="table">
    <tr><th>Başlık</th><th>Durum</th><th></th></tr>
    {% for y in yazilar %}
      <tr>
        <td>{{ y.baslik }}</td>
        <td>{% if y.yayinda %}Yayında{% else %}Taslak{% endif %}</td>
        <td>
          <a href="{% url 'yazi_duzenle' y.pk %}">Düzenle</a> ·
          <a href="{% url 'yazi_sil' y.pk %}" class="text-danger">Sil</a>
        </td>
      </tr>
    {% empty %}
      <tr><td colspan="3">Henüz yazınız yok.</td></tr>
    {% endfor %}
  </table>
{% endblock %}
""",
    "blog/templates/blog/yazi_sil.html": """{% extends "blog/base.html" %}

{% block icerik %}
  <h1>Yazıyı sil</h1>
  <p class="lead">“{{ yazi.baslik }}” silinecek. Bu işlem geri alınamaz.</p>
  <form method="post">
    {% csrf_token %}
    <button class="btn btn-danger">Evet, sil</button>
    <a href="{% url 'panel' %}" class="btn btn-link">Vazgeç</a>
  </form>
{% endblock %}
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")
