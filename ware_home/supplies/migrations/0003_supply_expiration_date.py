# Generated by Django 5.0 on 2024-05-10 15:01

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supplies", "0002_alter_category_options_alter_supply_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="supply",
            name="expiration_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 5, 10, 15, 1, 12, 350068, tzinfo=datetime.timezone.utc
                )
            ),
            preserve_default=False,
        ),
    ]