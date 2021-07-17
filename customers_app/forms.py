from django import forms
from localflavor.tr.forms import TRIdentificationNumberField
from localflavor.tr.tr_provinces import PROVINCE_CHOICES

from .models import Customer

class CustomerForm(forms.ModelForm):
    tr_id = TRIdentificationNumberField(label="TC Kimlik Numarası")

    class Meta:
        model = Customer
        fields = "__all__"

class CustomerSearchForm(forms.Form):
    pk = forms.IntegerField(label="ID", required=False)
    tr_id = forms.CharField(label="TC Kimlik Numarası", required=False)
    first_name = forms.CharField(label="Adı", required=False)
    last_name = forms.CharField(label="Soyadı", required=False)
    phone = forms.CharField(label="Telefon Numarası", required=False)
    province = forms.ChoiceField(label="İl", choices=(
        (None, ""), *PROVINCE_CHOICES), required=False, initial=None)
    district = forms.CharField(label="İlçe", required=False)

    page_size = forms.IntegerField(
        label="Sayfa Boyutu", min_value=1, initial=25)
