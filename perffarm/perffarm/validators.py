from datetime import datetime
from django.core.exceptions import ValidationError


def ValidateDate(date):

    if date > datetime.now():
        raise ValidationError(_('%(date)s is in the future'), params={'value': value}, )

    if date.year < 2020 or date.month < 8:
        raise ValidationError(_('%(date)s is too far in the past'), params={'value': value}, )
