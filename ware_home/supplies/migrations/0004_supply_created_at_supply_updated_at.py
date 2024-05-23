# Generated by Django 5.0 on 2024-05-22 13:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supplies", "0003_supply_expiration_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="supply",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="supply",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
