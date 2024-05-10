import datetime
import typing

from django.utils import timezone


class HasExpirationDate(typing.Protocol):
    expiration_date: datetime.date


def check_expiration_date(obj: HasExpirationDate) -> bool:
    return timezone.now().date() > obj.expiration_date + timezone.timedelta(
        days=1
    )


def get_expiration_days(obj: HasExpirationDate) -> int:
    return (obj.expiration_date - timezone.now().date()).days
