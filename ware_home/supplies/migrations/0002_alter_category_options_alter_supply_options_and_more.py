# Generated by Django 5.0 on 2024-05-10 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supplies", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
        migrations.AlterModelOptions(
            name="supply",
            options={"verbose_name_plural": "supplies"},
        ),
        migrations.AddField(
            model_name="product",
            name="bar_code",
            field=models.CharField(default="", max_length=63),
            preserve_default=False,
        ),
    ]
