# =============================================================================
# Python Kursu — Ders 26 (Hafta 13, Gün 2)
# Konu: Sanal ortam, Django kurulumu, startproject/startapp, proje yapısı, runserver, MVT, ilk view ve URL, model, migration, ORM ve SQL, superuser, admin paneli ve özelleştirme, Django shell — blog iskeleti
# Ortam: VS Code + Python 3.12 (Python ve Jupyter eklentileri)
#
# Nasıl kullanılır?
#   - "# %%" ile başlayan her satır yeni bir HÜCRE başlatır; üstündeki
#     "Run Cell" ile yalnızca o hücreyi çalıştırabilirsiniz.
#   - Önce bir klasör açın, sanal ortam kurun ve Django'yu yükleyin (terminalde):
#   -     python -m venv .venv   →   Windows: .venv\Scripts\activate   |   macOS/Linux: source .venv/bin/activate
#   -     python -m pip install django
#   - Bu dosyadaki hücreler projeyi ADIM ADIM kurar: komutları sizin yerinize çalıştırır ve dosyaları yazar.
#   - Asıl öğrenme için aynı adımları terminalde ve VS Code'da kendiniz de yapın; hücreler kontrol ve yedek içindir.
#   - Sunucuyu terminalde başlatın: python manage.py runserver   →   http://127.0.0.1:8000  (durdurmak: Ctrl+C)
#   - Örnek yönetici hesabı: admin / DersSifre-2026 — kendi projenizde güçlü ve size özel bir şifre seçin.
# =============================================================================


# %% Adım 1 — Proje oluştur (django-admin startproject sitem .)
import subprocess
import sys
from pathlib import Path

# Terminaldeki karşılığı: django-admin startproject sitem .
if not Path('manage.py').exists():
    subprocess.run([sys.executable, '-m', 'django', 'startproject', 'sitem', '.'], check=True)
else:
    print("manage.py zaten var, adım atlandı.")


# %% Adım 2 — Uygulama oluştur (startapp blog)
import subprocess
import sys
from pathlib import Path

# Terminaldeki karşılığı: python manage.py startapp blog
if not Path('blog').exists():
    subprocess.run([sys.executable, 'manage.py', 'startapp', 'blog'], check=True)
else:
    print("blog zaten var, adım atlandı.")


# %% Adım 3 — settings.py: INSTALLED_APPS'e blog, Türkçe dil ve saat dilimi
from pathlib import Path

ayar = Path("sitem/settings.py")
metin = ayar.read_text(encoding="utf-8")
degisiklikler = [
    ('    "django.contrib.staticfiles",\n]', '    "django.contrib.staticfiles",\n    "blog",\n]'),
    ('LANGUAGE_CODE = "en-us"', 'LANGUAGE_CODE = "tr"'),
    ('TIME_ZONE = "UTC"', 'TIME_ZONE = "Europe/Istanbul"'),
]
for eski, yeni in degisiklikler:
    if yeni not in metin:
        metin = metin.replace(eski, yeni)
ayar.write_text(metin, encoding="utf-8")
print("settings.py güncellendi" if '"blog"' in metin else "UYARI: elle düzenleyin")


# %% Adım 4 — İlk view ve URL'ler (blog/views.py, blog/urls.py, sitem/urls.py)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.http import HttpResponse


def ana_sayfa(request):
    return HttpResponse("<h1>Merhaba, Django!</h1>")
""",
    "blog/urls.py": """from django.urls import path

from . import views

urlpatterns = [
    path("", views.ana_sayfa, name="ana_sayfa"),
]
""",
    "sitem/urls.py": """from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 5 — Model (blog/models.py)
from pathlib import Path

dosyalar = {
    "blog/models.py": """from django.db import models


class Yazi(models.Model):
    baslik = models.CharField("Başlık", max_length=200)
    icerik = models.TextField("İçerik")
    olusturma = models.DateTimeField("Oluşturulma", auto_now_add=True)
    yayinda = models.BooleanField("Yayında", default=False)

    class Meta:
        verbose_name = "Yazı"
        verbose_name_plural = "Yazılar"
        ordering = ["-olusturma"]

    def __str__(self):
        return self.baslik
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 6a — makemigrations
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'makemigrations', 'blog'], check=True)


# %% Adım 6b — migrate
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)


# %% Adım 7 — Yönetici hesabı (createsuperuser, etkileşimsiz)
import os
import subprocess
import sys

# Terminaldeki karşılığı (önerilen): python manage.py createsuperuser
ortam = dict(os.environ, DJANGO_SUPERUSER_USERNAME="admin",
             DJANGO_SUPERUSER_EMAIL="admin@ornek.com", DJANGO_SUPERUSER_PASSWORD="DersSifre-2026")
sonuc = subprocess.run([sys.executable, "manage.py", "createsuperuser", "--noinput"],
                       env=ortam, capture_output=True, text=True)
print(sonuc.stdout or sonuc.stderr.strip().splitlines()[-1])


# %% Adım 8 — Admin kaydı (blog/admin.py)
from pathlib import Path

dosyalar = {
    "blog/admin.py": """from django.contrib import admin

from .models import Yazi


@admin.register(Yazi)
class YaziAdmin(admin.ModelAdmin):
    list_display = ("baslik", "yayinda", "olusturma")
    list_filter = ("yayinda",)
    search_fields = ("baslik", "icerik")
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Adım 9 — ORM denemesi (manage.py shell -c)
import subprocess
import sys

# Terminaldeki karşılığı: python manage.py shell  →  aşağıdaki satırları tek tek yazın
kod = """from blog.models import Yazi

Yazi.objects.create(baslik="İlk yazım", icerik="Merhaba!",
                    yayinda=True)
Yazi.objects.create(baslik="Taslak", icerik="Yarın bitecek.")
print(Yazi.objects.count())
print(Yazi.objects.all())
print(Yazi.objects.filter(yayinda=True))
print(Yazi.objects.get(pk=1).baslik)
Yazi.objects.filter(baslik="Taslak").update(yayinda=True)
print(Yazi.objects.filter(yayinda=True).count())"""
subprocess.run([sys.executable, "manage.py", "shell", "-c", kod], check=True)


# %% Adım 10 — Ana sayfa veritabanını okuyor (blog/views.py)
from pathlib import Path

dosyalar = {
    "blog/views.py": """from django.http import HttpResponse

from .models import Yazi


def ana_sayfa(request):
    sayi = Yazi.objects.filter(yayinda=True).count()
    html = f"<h1>Blogum</h1><p>Yayında {sayi} yazı var.</p>"
    return HttpResponse(html)
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 1 — çözüm (ozet alanı) — ardından makemigrations + migrate
from pathlib import Path

dosyalar = {
    "blog/models.py": """from django.db import models


class Yazi(models.Model):
    baslik = models.CharField("Başlık", max_length=200)
    ozet = models.CharField("Özet", max_length=300, blank=True)
    icerik = models.TextField("İçerik")
    olusturma = models.DateTimeField("Oluşturulma", auto_now_add=True)
    yayinda = models.BooleanField("Yayında", default=False)

    class Meta:
        verbose_name = "Yazı"
        verbose_name_plural = "Yazılar"
        ordering = ["-olusturma"]

    def __str__(self):
        return self.baslik
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 1 — makemigrations
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'makemigrations', 'blog'], check=True)


# %% Alıştırma 1 — migrate
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)


# %% Alıştırma 2 — çözüm (blog/admin.py)
from pathlib import Path

dosyalar = {
    "blog/admin.py": """from django.contrib import admin

from .models import Yazi


@admin.register(Yazi)
class YaziAdmin(admin.ModelAdmin):
    list_display = ("baslik", "ozet", "yayinda", "olusturma")
    list_filter = ("yayinda",)
    list_editable = ("yayinda",)
    search_fields = ("baslik", "icerik")
    date_hierarchy = "olusturma"
    list_per_page = 20
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 3 — çözüm (Proje modeli ve admin)
from pathlib import Path

dosyalar = {
    "blog/models.py": """from django.db import models


class Yazi(models.Model):
    baslik = models.CharField("Başlık", max_length=200)
    ozet = models.CharField("Özet", max_length=300, blank=True)
    icerik = models.TextField("İçerik")
    olusturma = models.DateTimeField("Oluşturulma", auto_now_add=True)
    yayinda = models.BooleanField("Yayında", default=False)

    class Meta:
        verbose_name = "Yazı"
        verbose_name_plural = "Yazılar"
        ordering = ["-olusturma"]

    def __str__(self):
        return self.baslik


class Proje(models.Model):
    ad = models.CharField("Ad", max_length=100)
    aciklama = models.TextField("Açıklama", blank=True)
    baglanti = models.URLField("Bağlantı", blank=True)
    tarih = models.DateField("Tarih")

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"
        ordering = ["-tarih"]

    def __str__(self):
        return self.ad
""",
    "blog/admin.py": """from django.contrib import admin

from .models import Proje, Yazi


@admin.register(Yazi)
class YaziAdmin(admin.ModelAdmin):
    list_display = ("baslik", "ozet", "yayinda", "olusturma")
    list_filter = ("yayinda",)
    list_editable = ("yayinda",)
    search_fields = ("baslik", "icerik")
    date_hierarchy = "olusturma"
    list_per_page = 20


@admin.register(Proje)
class ProjeAdmin(admin.ModelAdmin):
    list_display = ("ad", "tarih", "baglanti")
""",
}
for ad, icerik in dosyalar.items():
    Path(ad).parent.mkdir(parents=True, exist_ok=True)
    Path(ad).write_text(icerik, encoding="utf-8")
    print(ad, "yazıldı")


# %% Alıştırma 3 — makemigrations
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'makemigrations', 'blog'], check=True)


# %% Alıştırma 3 — migrate
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)


# %% Alıştırma 3 — shell sorguları
import subprocess
import sys

kod = """from datetime import date
from blog.models import Proje

Proje.objects.create(ad="Bütçe paneli", tarih=date(2026, 10, 22))
Proje.objects.create(ad="Ev ilanları", tarih=date(2026, 10, 20))
Proje.objects.create(ad="Tanıtım sayfası", tarih=date(2026, 10, 25))
print(Proje.objects.count(), "proje")
print(Proje.objects.first())
print(Proje.objects.filter(tarih__gte=date(2026, 10, 21)))"""
subprocess.run([sys.executable, "manage.py", "shell", "-c", kod], check=True)
