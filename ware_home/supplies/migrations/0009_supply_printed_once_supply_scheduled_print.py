# Generated by Django 5.0 on 2024-12-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supplies", "0008_demandtag"),
    ]

    operations = [
        migrations.AddField(
            model_name="supply",
            name="printed_once",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="supply",
            name="scheduled_print",
            field=models.BooleanField(default=False),
        ),
    ]
