# Generated by Django 4.1.3 on 2023-03-05 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopping_list", "0023_alter_order_order_num"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
