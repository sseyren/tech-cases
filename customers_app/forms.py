from django.forms import ModelForm
from localflavor.tr.forms import TRIdentificationNumberField

from .models import Customer

class CustomerForm(ModelForm):
    tr_id = TRIdentificationNumberField(label="TC Kimlik Numarası")

    class Meta:
        model = Customer
        fields = ["tr_id", "first_name", "last_name", "phone", "province", "district"]