# Generated by Django 4.1.3 on 2023-03-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopping_list", "0022_alter_order_order_num"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_num",
            field=models.IntegerField(default=""),
        ),
    ]
