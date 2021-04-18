from datetime import date

from django.core.exceptions import ValidationError


def no_past(value):
    today = date.today()
    if value < today:
        raise ValidationError("The agenda should contain a valid" " date (from today onwards)")
