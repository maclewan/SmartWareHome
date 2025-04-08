import datetime
import typing

from django.utils import timezone


class HasExpirationDate(typing.Protocol):
    expiration_date: datetime.date


def check_expiration_date(obj: HasExpirationDate) -> bool:
    if obj.expiration_date is None:
        return False
    return timezone.now().date() > obj.expiration_date - timezone.timedelta(days=1)


def get_expiration_days(obj: HasExpirationDate) -> int | None:
    if obj.expiration_date is None:
        return None
    return (obj.expiration_date - timezone.now().date()).days
