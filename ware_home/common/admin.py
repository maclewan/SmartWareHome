from django.db import models


class AutoFilterHorizontalMixin:
    """
    Automatically updates all many_to_many fields' widgets using filter_horizontal property
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        many_to_many_field_names = [
            field.name
            for field in self.model._meta.get_fields()
            if isinstance(field, models.ManyToManyField)
        ]
        self.filter_horizontal = many_to_many_field_names
