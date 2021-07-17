from django.core.exceptions import ValidationError


def phone_number_validator(value):
    if not value.isnumeric():
        raise ValidationError("Telefon numarası sadece rakamlardan oluşmalı.")

    if len(value) != 10:
        raise ValidationError("Telefon numarası tam 10 hane olmalı.")

    if value[0] == "0":
        raise ValidationError("Telefon numarası 0 rakamı ile başlayamaz.")
