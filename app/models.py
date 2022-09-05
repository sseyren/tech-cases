from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class CompanyType(models.TextChoices):
    SOLE = "sole", _('Sole Proprietorship')  # Şahıs Şirketi
    SME = "sme", _('Small and Medium-Sized Enterprise')  # KOBİ
    CORP = "corp", _('Corporation')  # Büyük İşletme
    SCO = "cso", _('Civil Society Organization')  # STK


class Company(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    type = models.CharField(max_length=5, choices=CompanyType.choices)
    country = CountryField()
    url = models.URLField(blank=True)
    employee_count = models.PositiveIntegerField(default=0)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"
