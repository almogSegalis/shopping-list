# Generated by Django 4.1.3 on 2023-03-01 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopping_list", "0016_alter_order_order_time"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Order",
        ),
    ]