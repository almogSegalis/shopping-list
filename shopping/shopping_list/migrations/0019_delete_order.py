# Generated by Django 4.1.3 on 2023-03-01 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopping_list", "0018_order"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Order",
        ),
    ]
