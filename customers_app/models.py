from django.db import models
from django import urls
from localflavor.tr.tr_provinces import PROVINCE_CHOICES

class Customer(models.Model):
    tr_id = models.CharField("TC Kimlik Numarası", max_length=11, unique=True)
    first_name = models.CharField("Adı", max_length=50)
    last_name = models.CharField("Soyadı", max_length=50)
    phone = models.CharField("Telefon Numarası", max_length=10)
    province = models.CharField("İl", max_length=2, choices=PROVINCE_CHOICES)
    district = models.CharField("İlçe", max_length=20)

    def get_absolute_url(self):
        return urls.reverse("detail", kwargs={"pk": self.pk})